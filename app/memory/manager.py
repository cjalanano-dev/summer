from typing import List
from app.memory.storage import MemoryStorage
from app.memory.retrieval import MemoryRetrieval
from app.memory.models import MemoryRecord

class MemoryManager:
    """Public interface for managing and querying persistent symbolic memories."""
    
    def __init__(self, db_path: str):
        self.storage = MemoryStorage(db_path)
        self.retrieval = MemoryRetrieval()

    def remember(self, content: str, category: str = "general") -> int:
        """Add a new memory to storage."""
        return self.storage.insert(category, content)

    def forget(self, memory_id: int) -> bool:
        """Delete a memory by its ID."""
        return self.storage.delete(memory_id)

    def search(self, query: str) -> List[MemoryRecord]:
        """Search memories by keyword."""
        return self.storage.search(query)

    def list_memories(self) -> List[MemoryRecord]:
        """List all stored memories."""
        return self.storage.get_all()

    def retrieve_context(self, query: str) -> str:
        """Retrieve relevant memories formatted as prompt context block."""
        all_memories = self.storage.get_all()
        relevant = self.retrieval.rank_and_select(query, all_memories)
        if not relevant:
            return ""
            
        lines = []
        for mem in relevant:
            lines.append(f"- [{mem.category}] {mem.content} (ID: {mem.id})")
        return "\n[RECALLED LOCAL MEMORIES]\n" + "\n".join(lines) + "\n"
