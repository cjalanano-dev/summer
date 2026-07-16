from typing import Generator, Tuple
from app.ollama import stream_chat
from app.tools.manager import ToolManager

class Agent:
    """Implements the Agent Loop, mediating between conversation state, tools, and the LLM."""
    
    def __init__(self, tool_manager: ToolManager):
        self.tool_manager = tool_manager

    def run_loop(self, prompt: str) -> Generator[Tuple[str, str], None, None]:
        """Runs the main agent loop.
        
        Flow:
        1. Fetch tool schemas from ToolManager.
        2. Query LLM passing prompt and tool schemas.
        3. If LLM requests tool execution:
           a. Execute tool using ToolManager.
           b. Feed results back to LLM history.
           c. Loop back to step 2.
        4. If no tool is requested, stream response to user.
        """
        # For Version 0.1 (no tools yet), we bypass the loop and stream directly
        # In Version 0.4 (Tool Calling), this function will manage the state loop
        yield from stream_chat(prompt)
