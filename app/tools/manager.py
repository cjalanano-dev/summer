from typing import Dict, Any, List
from app.tools.base import BaseTool

class ToolManager:
    """Manages system tools, their registration, schemas, and execution."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool):
        """Register a new tool instance conforming to the BaseTool interface."""
        self._tools[tool.name] = tool

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return the JSON schemas for all registered tools."""
        return [tool.to_schema() for tool in self._tools.values()]

    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a registered tool by name with the given arguments."""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' is not registered.")
        return self._tools[name].execute(**arguments)
