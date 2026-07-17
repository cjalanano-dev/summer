import os
from typing import Optional, Tuple

class WorkspaceDetector:
    """Traverses directories upwards to find project root indicators."""
    
    ROOT_INDICATORS = {
        ".git",
        "pyproject.toml",
        "requirements.txt",
        "package.json",
        "Cargo.toml",
        "pom.xml",
        "build.gradle",
        "Makefile",
        "go.mod"
    }

    def __init__(self, start_path: str):
        self.start_path = os.path.abspath(start_path)

    def detect_project_root(self) -> Tuple[str, bool]:
        """Traverses parent directories looking for root indicator files. Returns (root_path, is_project)."""
        current = self.start_path
        while True:
            for indicator in self.ROOT_INDICATORS:
                if os.path.exists(os.path.join(current, indicator)):
                    return current, True
                    
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent
            
        return self.start_path, False
