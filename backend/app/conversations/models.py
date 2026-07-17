from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Conversation:
    id: str
    title: str
    created_at: str
    updated_at: str
    pinned: bool = False
    archived: bool = False


@dataclass
class Message:
    id: int
    conversation_id: str
    role: str
    content: str
    timestamp: str
    metadata: str = field(default_factory=lambda: "{}")
