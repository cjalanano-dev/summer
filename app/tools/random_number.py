import random
from typing import Dict, Any
from app.tools.base import BaseTool

class RandomNumberTool(BaseTool):
    """A tool that picks a random number in a given range."""

    @property
    def name(self) -> str:
        return "random_number"

    @property
    def description(self) -> str:
        return "Picks a random number between a minimum and maximum value (inclusive)."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "min_val": {
                    "type": "integer",
                    "description": "The minimum value (defaults to 1)"
                },
                "max_val": {
                    "type": "integer",
                    "description": "The maximum value (defaults to 100)"
                }
            },
            "required": []
        }

    def execute(self, min_val: int = 1, max_val: int = 100, **kwargs) -> Any:
        try:
            val_min = int(min_val)
            val_max = int(max_val)
            if val_min > val_max:
                val_min, val_max = val_max, val_min
            return str(random.randint(val_min, val_max))
        except Exception as e:
            return f"Error: Failed to pick random number. {str(e)}"
