from typing import Dict, Any
from app.tools.base import BaseTool
from app.memory.manager import MemoryManager

class RememberTool(BaseTool):
    """A tool that writes new facts to long-term memory."""

    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    @property
    def name(self) -> str:
        return "remember"

    @property
    def description(self) -> str:
        return "Saves a new fact, preference, goal, or routine to persistent long-term memory."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The exact fact or preference to remember, e.g., 'User prefers spaces over tabs'"
                },
                "category": {
                    "type": "string",
                    "description": "The category of the memory, e.g., 'preference', 'project', 'goal', 'routine' (defaults to 'general')"
                }
            },
            "required": ["content"]
        }

    def execute(self, content: str, category: str = "general", **kwargs) -> Any:
        try:
            mem_id = self.memory_manager.remember(content, category)
            return f"Successfully saved to memory with ID {mem_id}."
        except Exception as e:
            return f"Error: Failed to save memory. {str(e)}"

class ForgetTool(BaseTool):
    """A tool that deletes specific facts from long-term memory."""

    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    @property
    def name(self) -> str:
        return "forget"

    @property
    def description(self) -> str:
        return "Deletes a specific fact, preference, or goal from memory using its integer ID."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "memory_id": {
                    "type": "integer",
                    "description": "The integer ID of the memory to forget."
                }
            },
            "required": ["memory_id"]
        }

    def execute(self, memory_id: int, **kwargs) -> Any:
        try:
            success = self.memory_manager.forget(int(memory_id))
            if success:
                return f"Successfully deleted memory with ID {memory_id}."
            else:
                return f"Error: No memory found with ID {memory_id}."
        except Exception as e:
            return f"Error: Failed to delete memory. {str(e)}"
