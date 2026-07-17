from typing import Generator, Tuple, List, Dict
from app.llm import LLMClient
from app.tools.registry import ToolRegistry
from app.agent.planner import Planner
from app.agent.executor import Executor

class Agent:
    """Coordinates the Agent Loop, managing the lifecycle of prompt analysis, planning, and execution."""
    
    def __init__(self, llm_client: LLMClient, tool_registry: ToolRegistry):
        self.llm_client = llm_client
        self.tool_registry = tool_registry
        self.planner = Planner(self.llm_client)
        self.executor = Executor(self.tool_registry)

    def run_loop(self, prompt: str, history: List[Dict[str, str]], model: str = None) -> Generator[Tuple[str, str], None, None]:
        """Runs the agent loop step-by-step."""
        # 1. Ask planner to create a plan based on query, conversation history, and tools
        tools_schema = self.tool_registry.get_tool_schemas()
        plan = self.planner.create_plan(prompt, history, tools_schema, model=model)

        # 2. Check if a tool execution is needed
        temp_history = list(history)
        temp_history.append({"role": "user", "content": prompt})

        if plan.get("type") == "execute_tool":
            # Execute tool and feed result back to LLM context
            exec_result = self.executor.execute_plan(plan)
            
            if exec_result.get("status") == "success":
                tool_name = exec_result.get("tool_name")
                result_content = exec_result.get("result")
                
                # Yield a subtle notice to the UI so the user knows a tool was run
                yield "thinking", f"[Executing tool '{tool_name}'...]\n"
                
                # Append tool feedback context to LLM thread
                temp_history.append({
                    "role": "system",
                    "content": (
                        f"The user's request was processed by running the tool '{tool_name}'. "
                        f"Here is the execution result:\n"
                        f"--- START OF TOOL RESULT ---\n"
                        f"{result_content}\n"
                        f"--- END OF TOOL RESULT ---\n\n"
                        f"Please write a natural, clean response to the user summarizing or displaying this result. "
                        f"Do NOT output any function call syntax, JSON arguments, or tool commands."
                    )
                })
            else:
                error_msg = exec_result.get("error", "Unknown error")
                temp_history.append({
                    "role": "system",
                    "content": f"[Tool System Error]\nAn error occurred while executing tool '{plan.get('tool_name')}':\n{error_msg}"
                })

        # 3. Request stream response from LLM Client
        yield from self.llm_client.stream_chat(temp_history, model=model)
