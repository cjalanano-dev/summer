import os
from typing import Dict, Any, List
from app.tools.base import BaseTool

class ReadMultipleFilesTool(BaseTool):
    """Allows Summer to read the contents of multiple files at once."""

    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)

    @property
    def name(self) -> str:
        return "read_multiple_files"

    @property
    def description(self) -> str:
        return "Reads the contents of multiple text files inside the workspace in a single batch call. Rejects binary or files larger than 1MB."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "paths": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of relative or absolute file paths to read."
                }
            },
            "required": ["paths"]
        }

    def execute(self, paths: List[str], **kwargs) -> Any:
        if not paths:
            return "Error: No file paths specified."
            
        results = []
        for path in paths:
            try:
                target_path = os.path.abspath(os.path.join(self.workspace_root, path))
                if not target_path.startswith(self.workspace_root):
                    results.append(f"=== File: {path} ===\nError: Access denied. File is outside the workspace.\n")
                    continue
                    
                if not os.path.exists(target_path):
                    results.append(f"=== File: {path} ===\nError: File does not exist.\n")
                    continue
                    
                if not os.path.isfile(target_path):
                    results.append(f"=== File: {path} ===\nError: Not a file.\n")
                    continue
                    
                file_size = os.path.getsize(target_path)
                if file_size > 1024 * 1024:
                    results.append(f"=== File: {path} ===\nError: File size exceeds 1MB limit.\n")
                    continue
                    
                with open(target_path, "rb") as f:
                    chunk = f.read(1024)
                    if b"\x00" in chunk:
                        results.append(f"=== File: {path} ===\nError: File contains binary data and cannot be read as text.\n")
                        continue
                        
                with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                    results.append(f"=== File: {path} ===\n{content}\n")
            except Exception as e:
                results.append(f"=== File: {path} ===\nError: {str(e)}\n")
                
        return "\n".join(results)
