from dataclasses import dataclass

@dataclass
class MemoryRecord:
    """Represents a single symbolic memory fact stored in SQLite."""
    id: int
    category: str
    content: str
    created_at: str
