from typing import Generator, Tuple, List, Dict
from app.llm import LLMClient
from app.tools.manager import ToolManager
from app.agent.planner import Planner
from app.agent.executor import Executor

class Agent:
    """Coordinates the Agent Loop, managing the lifecycle of prompt analysis, planning, and execution."""
    
    def __init__(self, llm_client: LLMClient, tool_manager: ToolManager):
        self.llm_client = llm_client
        self.tool_manager = tool_manager
        self.planner = Planner()
        self.executor = Executor(self.tool_manager)

    def run_loop(self, prompt: str, history: List[Dict[str, str]]) -> Generator[Tuple[str, str], None, None]:
        """Runs the agent loop step-by-step."""
        # 1. Ask planner to create a plan based on query, conversation history, and tools
        tools_schema = self.tool_manager.get_tool_schemas()
        plan = self.planner.create_plan(prompt, history, tools_schema)

        # 2. Check if a tool execution is needed
        if plan.get("type") == "execute_tool":
            # Execute tool and feed result back to LLM (placeholder for V0.4)
            self.executor.execute_plan(plan)

        # 3. Request stream response from LLM Client
        # The agent adds the current prompt to the history temporarily for the query
        temp_history = list(history)
        temp_history.append({"role": "user", "content": prompt})
        
        yield from self.llm_client.stream_chat(temp_history)
