import os
from typing import List, Tuple

class WorkspaceScanner:
    """Crawls files and directories recursively inside the project root, skipping common noise."""
    
    IGNORE_DIRS = {
        ".git", ".github", ".venv", "venv", "node_modules", 
        "__pycache__", "build", "dist", "target", "out", ".idea", ".vscode",
        "summer.egg-info"
    }

    def __init__(self, root_path: str):
        self.root_path = os.path.abspath(root_path)

    def scan(self) -> Tuple[List[str], List[str], int]:
        """Returns (files, directories, total_size) with paths relative to the root_path."""
        files_list = []
        dirs_list = []
        total_size = 0
        
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS and not d.startswith(".")]
            
            for d in dirs:
                full_path = os.path.join(root, d)
                rel_path = os.path.relpath(full_path, self.root_path)
                dirs_list.append(rel_path.replace(os.sep, "/"))
                
            for f in files:
                if f.startswith("."):
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, self.root_path)
                files_list.append(rel_path.replace(os.sep, "/"))
                
                try:
                    total_size += os.path.getsize(full_path)
                except Exception:
                    pass
                
        return files_list, dirs_list, total_size
