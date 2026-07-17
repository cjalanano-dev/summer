import os
from typing import Dict, Any
from app.tools.base import BaseTool

class DirectoryListTool(BaseTool):
    """A tool that lists files and folders in a specified directory path safely."""

    @property
    def name(self) -> str:
        return "directory_list"

    @property
    def description(self) -> str:
        return "Lists files and directories in a specified path. Defaults to the current folder."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to list (defaults to the current working folder '.')"
                }
            },
            "required": []
        }

    def execute(self, path: str = ".", **kwargs) -> Any:
        try:
            target_path = os.path.abspath(path)
            if not os.path.exists(target_path):
                return f"Error: The path '{path}' does not exist."
            if not os.path.isdir(target_path):
                return f"Error: The path '{path}' is not a directory."

            items = os.listdir(target_path)
            if not items:
                return f"Directory '{target_path}' is empty."

            # Format items
            lines = []
            for item in sorted(items):
                item_path = os.path.join(target_path, item)
                item_type = "[DIR]" if os.path.isdir(item_path) else "[FILE]"
                size = ""
                if os.path.isfile(item_path):
                    size = f" ({os.path.getsize(item_path)} bytes)"
                lines.append(f"  {item_type} {item}{size}")

            return f"Contents of directory '{target_path}':\n" + "\n".join(lines)
        except Exception as e:
            return f"Error: Failed to list directory contents. {str(e)}"
