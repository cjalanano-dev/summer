# Project Summer Tool API

This document details the object-oriented Tool interface design.

## Base Class (`BaseTool`)

All tools must inherit from `BaseTool` (in `app/tools/base.py`) and implement the following properties and methods:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the tool used by the LLM."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A description of what the tool does and when to use it."""
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON Schema defining the expected parameters of the tool."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """The execution logic of the tool."""
        pass
```

## Tool Schema Generation

The `to_schema()` helper automatically packages tool specifications into an Ollama-compatible structure:
```json
{
  "type": "function",
  "function": {
    "name": "<name>",
    "description": "<description>",
    "parameters": <parameters>
  }
}
```

## Registry & Execution (`ToolManager`)

The `ToolManager` (in `app/tools/manager.py`) registers subclasses using `register_tool(tool_instance)` and executes them via `execute_tool(name, arguments)`. This isolates the execution of concrete functions from the model loop.
