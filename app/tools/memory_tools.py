from typing import Dict, Any
from app.tools.base import BaseTool
from app.memory.manager import MemoryManager

class RememberTool(BaseTool):
    """A tool that writes new structured facts to long-term memory."""

    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    @property
    def name(self) -> str:
        return "remember"

    @property
    def description(self) -> str:
        return "Saves a structured fact, preference, goal, or project detail to persistent long-term memory."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "The category of the memory. Must be one of: 'preference', 'person', 'project', 'goal', 'fact', 'routine', 'reminder', 'custom'."
                },
                "key": {
                    "type": "string",
                    "description": "The specific topic or identifier of the memory, e.g. 'editor', 'favorite_food', 'career'."
                },
                "value": {
                    "type": "string",
                    "description": "The content or value of the memory, e.g. 'VS Code', 'Pizza', 'Become Software Engineer'."
                },
                "importance": {
                    "type": "integer",
                    "description": "How important this memory is from 1 (low) to 5 (high). Defaults to 3."
                }
            },
            "required": ["category", "key", "value"]
        }

    def execute(self, category: str, key: str, value: str, importance: int = 3, **kwargs) -> Any:
        try:
            mem_id = self.memory_manager.remember(category, key, value, importance)
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
        return "Deletes specific facts, preferences, or goals from memory using an integer ID, category name, or key identifier."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "memory_id": {
                    "type": "integer",
                    "description": "The integer ID of the memory to forget (optional)."
                },
                "category": {
                    "type": "string",
                    "description": "Delete all memories in this category (optional)."
                },
                "key": {
                    "type": "string",
                    "description": "Delete memories matching this key (optional)."
                }
            }
        }

    def execute(self, memory_id: int = None, category: str = None, key: str = None, **kwargs) -> Any:
        try:
            success = self.memory_manager.forget(memory_id=memory_id, category=category, key=key)
            if success:
                target = f"ID {memory_id}" if memory_id is not None else (f"category '{category}'" if category is not None else f"key '{key}'")
                return f"Successfully deleted memory matching {target}."
            else:
                return "Error: No matching memory found or deletion failed."
        except Exception as e:
            return f"Error: Failed to delete memory. {str(e)}"
