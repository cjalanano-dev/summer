import uuid
from typing import Dict, Any
from app.tools.base import BaseTool

class UUIDGeneratorTool(BaseTool):
    """A tool that generates v4 UUIDs."""

    @property
    def name(self) -> str:
        return "uuid_generator"

    @property
    def description(self) -> str:
        return "Generates a unique, random UUID (v4)."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

    def execute(self, **kwargs) -> Any:
        return str(uuid.uuid4())
