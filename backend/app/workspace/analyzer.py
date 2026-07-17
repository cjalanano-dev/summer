import os
import fnmatch
from typing import List, Dict, Any, Tuple

class WorkspaceAnalyzer:
    """Inspects project structure to determine project type, languages, and dependencies."""
    
    IMPORTANT_FILE_PATTERNS = [
        "readme.md", "readme.txt", "readme",
        "requirements.txt", "pyproject.toml",
        "package.json", "dockerfile", "docker-compose.yml",
        ".env.example", "license", "makefile", "config.*"
    ]

    def __init__(self, root_path: str):
        self.root_path = root_path

    def analyze(self, files: List[str]) -> Tuple[str, List[str], Dict[str, Any]]:
        """Returns (project_type, important_files, metadata_dict)."""
        project_type = "unknown"
        metadata = {}
        
        # Detect languages based on file extensions
        extensions = {}
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext:
                extensions[ext] = extensions.get(ext, 0) + 1
                  
        metadata["extensions"] = extensions
        
        # Root indicator checks
        if "Cargo.toml" in files:
            project_type = "Rust Cargo Project"
        elif "package.json" in files:
            project_type = "Node.js Project"
        elif "pyproject.toml" in files:
            project_type = "Python Project (Poetry/Pipenv/Flit)"
        elif "requirements.txt" in files:
            project_type = "Python Project (Pip)"
        elif "setup.py" in files:
            project_type = "Python Project (Setuptools)"
        elif "pom.xml" in files:
            project_type = "Java Maven Project"
        elif "build.gradle" in files:
            project_type = "Java Gradle Project"
        elif "go.mod" in files:
            project_type = "Go Module Project"
        elif "CMakeLists.txt" in files:
            project_type = "C/C++ CMake Project"
        elif "Makefile" in files:
            project_type = "Makefile Project"
              
        # Identify important files
        important_files = []
        for f in files:
            basename = os.path.basename(f).lower()
            for pattern in self.IMPORTANT_FILE_PATTERNS:
                if fnmatch.fnmatch(basename, pattern):
                    important_files.append(f)
                    break
                    
        readme_file = next((f for f in important_files if "readme" in os.path.basename(f).lower()), None)
        if readme_file:
            metadata["readme"] = readme_file
              
        return project_type, important_files, metadata
