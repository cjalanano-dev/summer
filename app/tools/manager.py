from typing import Dict, Any, Callable, List

class ToolManager:
    """Manages system tools, their registration, schemas, and execution."""
    
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: List[Dict[str, Any]] = []

    def register_tool(self, schema: Dict[str, Any], func: Callable):
        """Register a new tool with its JSON schema definition and python implementation."""
        name = schema.get("function", {}).get("name")
        if name:
            self._tools[name] = func
            self._schemas.append(schema)

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return the JSON schemas for all registered tools."""
        return self._schemas

    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a registered tool by name with the given arguments."""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' is not registered.")
        return self._tools[name](**arguments)
