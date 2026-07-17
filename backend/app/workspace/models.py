from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Workspace:
    """Represents the context and structures of the active developer project workspace."""
    root_path: str
    project_name: str
    project_type: str
    git_repository: bool
    files: List[str] = field(default_factory=list)
    directories: List[str] = field(default_factory=list)
    important_files: List[str] = field(default_factory=list)
    total_size: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
