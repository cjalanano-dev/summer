import os
import fnmatch
from typing import Dict, Any, List
from app.tools.base import BaseTool

class SearchFilesTool(BaseTool):
    """Allows Summer to locate files in the workspace matching a pattern."""

    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)

    @property
    def name(self) -> str:
        return "search_files"

    @property
    def description(self) -> str:
        return "Finds files matching a glob pattern (e.g. '*.py') inside a workspace directory, optionally recursively."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to search inside (relative to workspace root). Defaults to the workspace root '.'."
                },
                "pattern": {
                    "type": "string",
                    "description": "The glob pattern to match, e.g. '*.toml', 'requirements.txt'."
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Whether to search recursively in subdirectories. Defaults to true."
                }
            },
            "required": ["pattern"]
        }

    def execute(self, pattern: str, directory: str = ".", recursive: bool = True, **kwargs) -> Any:
        try:
            search_dir = os.path.abspath(os.path.join(self.workspace_root, directory))
            if not search_dir.startswith(self.workspace_root):
                return "Error: Access denied. You can only search within the workspace."
                
            if not os.path.exists(search_dir) or not os.path.isdir(search_dir):
                return f"Error: Search directory '{directory}' does not exist or is not a directory."

            matches: List[str] = []
            
            if recursive:
                for root, dirs, files in os.walk(search_dir):
                    dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("venv", ".venv", "__pycache__", "node_modules")]
                    for filename in fnmatch.filter(files, pattern):
                        full_path = os.path.join(root, filename)
                        rel_path = os.path.relpath(full_path, self.workspace_root)
                        matches.append(rel_path)
            else:
                try:
                    for filename in os.listdir(search_dir):
                        if os.path.isfile(os.path.join(search_dir, filename)) and fnmatch.fnmatch(filename, pattern):
                            rel_path = os.path.relpath(os.path.join(search_dir, filename), self.workspace_root)
                            matches.append(rel_path)
                except Exception as e:
                    return f"Error: Failed to list directory contents. {str(e)}"
                    
            if not matches:
                return f"No files matching pattern '{pattern}' found."
                
            return "\n".join(matches)
        except Exception as e:
            return f"Error: Failed to search files. {str(e)}"
