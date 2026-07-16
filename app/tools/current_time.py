import datetime
from typing import Dict, Any
from app.tools.base import BaseTool

class CurrentTimeTool(BaseTool):
    """A tool that retrieves the current system date and time."""

    @property
    def name(self) -> str:
        return "current_time"

    @property
    def description(self) -> str:
        return "Returns the current local date and time."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

    def execute(self, **kwargs) -> Any:
        now = datetime.datetime.now()
        return now.strftime("%B %d, %Y, %I:%M %p")
