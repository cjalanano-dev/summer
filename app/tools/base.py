from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    """Abstract base class representing a unified Tool interface."""
    
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

    def to_schema(self) -> Dict[str, Any]:
        """Convert the tool definition to Ollama-compatible JSON schema format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
