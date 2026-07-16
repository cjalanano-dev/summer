from typing import Generator, Tuple
from app.agent import Agent
from app.tools.manager import ToolManager

class ConversationManager:
    """Manages conversation state and coordinates between the CLI and the LLM Client."""
    
    def __init__(self, model: str = None):
        self.model = model
        self.tool_manager = ToolManager()
        self.agent = Agent(self.tool_manager)

    def send_message(self, prompt: str) -> Generator[Tuple[str, str], None, None]:
        """Send a user message and yield the streamed response (chunk_type, text)."""
        yield from self.agent.run_loop(prompt)
