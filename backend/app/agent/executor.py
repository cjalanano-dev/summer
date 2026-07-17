from typing import Dict, Any
from app.tools.registry import ToolRegistry

class Executor:
    """Executes tasks, runs tools, and aggregates the results."""
    
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches tasks and collects outputs."""
        if plan.get("type") != "execute_tool":
            return {}
            
        tool_name = plan.get("tool_name")
        arguments = plan.get("arguments", {})
        
        try:
            result = self.tool_registry.execute_tool(tool_name, arguments)
            return {
                "status": "success",
                "tool_name": tool_name,
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "tool_name": tool_name,
                "error": str(e)
            }
