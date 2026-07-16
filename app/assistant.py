import os
import datetime
from typing import Generator, Tuple
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
from app.memory.manager import MemoryManager
from app.agent.agent import Agent
from app.conversation import Conversation

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
        self.memory = MemoryManager(os.path.join(self.config.project_root, "data", "memory.db"))
        
        # Register Memory tools
        self.tool_registry.register_tool(RememberTool(self.memory))
        self.tool_registry.register_tool(ForgetTool(self.memory))
        
        self.agent = Agent(self.llm_client, self.tool_registry)
        self.conversation = Conversation(self.config.system_prompt)

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

    def chat(self, prompt: str) -> Generator[Tuple[str, str], None, None]:
        """Send a user message, yield response chunks, and update persistent history."""
        # Log user query
        self._log_interaction("user", prompt)

        # Retrieve relevant memories and inject them as system context
        memory_context = self.memory.retrieve_context(prompt)
        temp_messages = list(self.conversation.messages)
        if memory_context:
            temp_messages.append({"role": "system", "content": memory_context})

        # 1. Run agent loop with current query and conversation history
        full_response = []
        for chunk_type, text in self.agent.run_loop(prompt, temp_messages):
            yield chunk_type, text
            if chunk_type == "content":
                full_response.append(text)

        # 2. Persist the turn to history once successfully finished
        response_str = "".join(full_response)
        if response_str:
            self.conversation.add_user(prompt)
            self.conversation.add_assistant(response_str)
            # Log assistant response
            self._log_interaction("summer", response_str)
