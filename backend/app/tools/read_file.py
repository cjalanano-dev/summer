import os
from typing import Dict, Any
from app.tools.base import BaseTool

class ReadFileTool(BaseTool):
    """Allows Summer to read the contents of a file safely."""

    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Reads the content of a text file inside the workspace safely. Rejects files larger than 1MB or binary formats."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative or absolute path of the file to read."
                }
            },
            "required": ["path"]
        }

    def execute(self, path: str, **kwargs) -> Any:
        try:
            target_path = os.path.abspath(os.path.join(self.workspace_root, path))
            if not target_path.startswith(self.workspace_root):
                return "Error: Access denied. You can only read files within the workspace."
                
            if not os.path.exists(target_path):
                return f"Error: File '{path}' does not exist."
                
            if not os.path.isfile(target_path):
                return f"Error: '{path}' is not a file."
                
            file_size = os.path.getsize(target_path)
            if file_size > 1024 * 1024:
                return f"Error: File size is {file_size / (1024*1024):.2f}MB, which exceeds the 1MB limit."
                
            with open(target_path, "rb") as f:
                chunk = f.read(1024)
                if b"\x00" in chunk:
                    return "Error: File contains binary data and cannot be read as text."
                    
            with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        except Exception as e:
            return f"Error: Failed to read file. {str(e)}"
