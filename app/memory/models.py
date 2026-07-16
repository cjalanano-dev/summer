from dataclasses import dataclass

@dataclass
class MemoryRecord:
    """Represents a single structured symbolic memory fact stored in SQLite."""
    id: int
    category: str
    key: str
    value: str
    importance: int
    created_at: str
    updated_at: str
