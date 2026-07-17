import os
import datetime
import json
import re
from typing import Generator, Tuple, List, Dict, Optional
from app.config import Config
from app.llm import LLMClient
from app.tools.registry import ToolRegistry
from app.tools.calculator import CalculatorTool
from app.tools.current_time import CurrentTimeTool
from app.tools.random_number import RandomNumberTool
from app.tools.uuid_gen import UUIDGeneratorTool
from app.tools.password import PasswordGeneratorTool
from app.tools.system_info import SystemInfoTool
from app.tools.directory_list import DirectoryListTool
from app.tools.memory_tools import RememberTool, ForgetTool
from app.tools.read_file import ReadFileTool
from app.tools.search_files import SearchFilesTool
from app.tools.read_multiple_files import ReadMultipleFilesTool
from app.tools.clipboard import ClipboardTool
from app.memory.manager import MemoryManager
from app.workspace.manager import WorkspaceManager
from app.tools.workspace_summary import WorkspaceSummaryTool
from app.agent.agent import Agent
from app.conversations.manager import ConversationManager

class Summer:
    """Main coordinator representing Summer. Orchestrates configuration, LLM, agent, and conversation history."""
    
    def __init__(self):
        self.config = Config()
        self.llm_client = LLMClient(self.config)
        self.tool_registry = ToolRegistry()
        
        # Register default tool plugins
        self.tool_registry.register_tool(CalculatorTool())
        self.tool_registry.register_tool(CurrentTimeTool())
        self.tool_registry.register_tool(RandomNumberTool())
        self.tool_registry.register_tool(UUIDGeneratorTool())
        self.tool_registry.register_tool(PasswordGeneratorTool())
        self.tool_registry.register_tool(SystemInfoTool())
        self.tool_registry.register_tool(DirectoryListTool())
        
        # Initialize Memory Subsystem
        self.memory = MemoryManager(os.path.join(self.config.project_root, "data", "summer.db"))
        
        # Register Memory tools
        self.tool_registry.register_tool(RememberTool(self.memory))
        self.tool_registry.register_tool(ForgetTool(self.memory))
        
        # Register workspace & clipboard tools
        self.tool_registry.register_tool(ReadFileTool(self.config.project_root))
        self.tool_registry.register_tool(SearchFilesTool(self.config.project_root))
        self.tool_registry.register_tool(ReadMultipleFilesTool(self.config.project_root))
        self.tool_registry.register_tool(ClipboardTool())
        
        # Initialize Workspace subsystem
        self.workspace = WorkspaceManager(self.config.project_root)
        
        # Register workspace summary tool
        self.tool_registry.register_tool(WorkspaceSummaryTool(self.workspace))
        
        self.agent = Agent(self.llm_client, self.tool_registry)
        self.conversation_manager = ConversationManager(
            os.path.join(self.config.project_root, "data", "summer.db")
        )
        self.current_messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.config.system_prompt}
        ]

    def _log_interaction(self, role: str, content: str):
        """Append interaction details with timestamp to a log file."""
        try:
            log_dir = os.path.join(self.config.project_root, "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "summer.log")
            
            # Format time as [20:15]
            timestamp = datetime.datetime.now().strftime("%H:%M")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}]\n{role.capitalize()}:\n{content}\n\n")
        except Exception:
            pass

    def chat(
        self,
        prompt: str,
        model: Optional[str] = None,
        conversation_id: Optional[str] = None,
    ) -> Generator[Tuple[str, str], None, None]:
        """Send a user message, yield response chunks, and update persistent history.
        
        If conversation_id is provided, messages are persisted to the database.
        Otherwise, in-memory (legacy) behavior is used.
        """
        self._log_interaction("user", prompt)

        memory_context = self.memory.retrieve_context(prompt)
        workspace_context = f"\n[CURRENT WORKSPACE CONTEXT]\n{self.workspace.summary()}\n"

        # Build message list for the LLM
        temp_messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.config.system_prompt}
        ]

        if conversation_id:
            db_messages = self.conversation_manager.get_messages(conversation_id)
            for m in db_messages:
                temp_messages.append({"role": m.role, "content": m.content})
        else:
            temp_messages.extend(self.current_messages[1:])

        temp_messages.append({"role": "system", "content": workspace_context})
        if memory_context:
            temp_messages.append({"role": "system", "content": memory_context})

        full_response = []
        for chunk_type, text in self.agent.run_loop(prompt, temp_messages, model=model):
            yield chunk_type, text
            if chunk_type == "content":
                full_response.append(text)

        response_str = "".join(full_response)
        if response_str:
            self._log_interaction("summer", response_str)
            self._extract_and_store_memory_async(prompt, response_str)

            if conversation_id:
                self.conversation_manager.add_message(conversation_id, "user", prompt)
                self.conversation_manager.add_message(
                    conversation_id, "assistant", response_str
                )
                self._auto_title(conversation_id)
            else:
                self.current_messages.append({"role": "user", "content": prompt})
                self.current_messages.append(
                    {"role": "assistant", "content": response_str}
                )

    def _auto_title(self, conversation_id: str):
        """Generate a short title using the LLM after the second user message."""
        conv = self.conversation_manager.load(conversation_id)
        if not conv or conv.title != "New Chat":
            return

        messages = self.conversation_manager.get_messages(conversation_id)
        user_msgs = [m for m in messages if m.role == "user"]
        assistant_msgs = [m for m in messages if m.role == "assistant"]

        if len(user_msgs) < 2 or not assistant_msgs:
            return

        exchange = []
        for m in messages:
            if m.role == "user":
                exchange.append(f"User: {m.content[:300]}")
            elif m.role == "assistant":
                exchange.append(f"Assistant: {m.content[:300]}")

        prompt_text = (
            "Generate a very short, specific title (maximum 5 words) for this conversation. "
            "Return ONLY the title text, no quotes, no labels, no punctuation at the end.\n\n"
            f"{chr(10).join(exchange)}\n\n"
            "Title:"
        )

        try:
            response = self.llm_client.chat(
                [{"role": "user", "content": prompt_text}]
            ).strip()
            title = response.strip("\"'").strip()
            if title:
                self.conversation_manager.rename(conversation_id, title[:100])
        except Exception:
            pass

    def _extract_and_store_memory_async(self, user_msg: str, assistant_msg: str):
        """Analyze the exchange and automatically extract structured long-term memories."""
        system_prompt = (
            "You are Summer's Automatic Memory Extraction Agent. Your job is to analyze the dialogue exchange "
            "and determine if the user has shared any new facts, preferences, goals, project info, routines, "
            "reminders, or details about people that are worth saving for long-term reference.\n\n"
            "INSTRUCTIONS:\n"
            "You must output a single, valid JSON block matching one of the following two schemas:\n\n"
            "If there is nothing new or important to remember, return:\n"
            "{\n"
            '  "store": false\n'
            "}\n\n"
            "If there is something worth remembering, return:\n"
            "{\n"
            '  "store": true,\n'
            '  "category": "preference" | "person" | "project" | "goal" | "fact" | "routine" | "reminder" | "custom",\n'
            '  "key": "<short_camelcase_or_snakecase_identifier>",\n'
            '  "value": "<the_exact_fact_value_to_remember>",\n'
            '  "importance": <integer_importance_from_1_to_5>\n'
            "}\n\n"
            "CRITICAL: Do NOT output any markdown tags (like ```json or ```) or other text. Only return the JSON block."
        )
        
        user_context = f"User message: \"{user_msg}\"\nAssistant response: \"{assistant_msg}\""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_context}
        ]
        
        try:
            response = self.llm_client.chat(messages).strip()
            if response.startswith("```"):
                response = re.sub(r"^```(?:json)?\n", "", response)
                response = re.sub(r"\n```$", "", response)
            response = response.strip()
            
            data = json.loads(response)
            if isinstance(data, dict) and data.get("store") is True:
                cat = data.get("category", "custom")
                key = data.get("key", "")
                val = data.get("value", "")
                imp = data.get("importance", 3)
                if key and val:
                    self.memory.remember(cat, key, val, imp)
        except Exception:
            pass
