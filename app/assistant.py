from typing import Generator, Tuple
from app.config import Config
from app.llm import LLMClient
from app.tools.manager import ToolManager
from app.agent.agent import Agent
from app.conversation import Conversation

class Assistant:
    """Main coordinator representing Summer. Orchestrates configuration, LLM, agent, and conversation history."""
    
    def __init__(self):
        self.config = Config()
        self.llm_client = LLMClient(self.config)
        self.tool_manager = ToolManager()
        self.agent = Agent(self.llm_client, self.tool_manager)
        self.conversation = Conversation(self.config.system_prompt)

    def send_message(self, prompt: str) -> Generator[Tuple[str, str], None, None]:
        """Send a user message, yield response chunks, and update persistent history."""
        # 1. Run agent loop with current query and conversation history
        full_response = []
        for chunk_type, text in self.agent.run_loop(prompt, self.conversation.get_messages()):
            yield chunk_type, text
            if chunk_type == "content":
                full_response.append(text)

        # 2. Persist the turn to history once successfully finished
        response_str = "".join(full_response)
        if response_str:
            self.conversation.add_message("user", prompt)
            self.conversation.add_message("assistant", response_str)
