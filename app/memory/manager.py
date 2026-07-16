from typing import List
from app.memory.storage import MemoryStorage
from app.memory.retrieval import MemoryRetrieval
from app.memory.models import MemoryRecord

class MemoryManager:
    """Public interface for managing and querying persistent symbolic key-value memories."""
    
    # Predefined valid categories
    CATEGORIES = {
        "preference",
        "person",
        "project",
        "goal",
        "fact",
        "routine",
        "reminder",
        "custom"
    }

    def __init__(self, db_path: str):
        self.storage = MemoryStorage(db_path)
        self.retrieval = MemoryRetrieval()

    def remember(self, category: str, key: str, value: str, importance: int = 3) -> int:
        """Add or replace a memory record in a structured category."""
        cat_clean = category.strip().lower()
        if cat_clean not in self.CATEGORIES:
            cat_clean = "custom"
        return self.storage.insert_or_update(cat_clean, key.strip(), value.strip(), importance)

    def forget(self, memory_id: int = None, category: str = None, key: str = None) -> bool:
        """Delete memories matching the specified ID, category, or key attribute."""
        if memory_id is not None:
            return self.storage.delete(memory_id)
        if category is not None:
            return self.storage.delete_by_category(category.strip().lower())
        if key is not None:
            return self.storage.delete_by_key(key.strip())
        return False

    def forget_all(self):
        """Delete all stored memories."""
        self.storage.clear_all()

    def search(self, query: str) -> List[MemoryRecord]:
        """Search memories by keyword matching key or value."""
        return self.storage.search(query)

    def list_memories(self) -> List[MemoryRecord]:
        """List all stored memories."""
        return self.storage.get_all()

    def list(self) -> List[MemoryRecord]:
        """API list helper returning all stored memories."""
        return self.storage.get_all()

    def get(self, memory_id: int) -> MemoryRecord:
        """API get helper fetching a record by ID."""
        return self.storage.get_by_id(memory_id)

    def update(self, memory_id: int, category: str = None, key: str = None, value: str = None, importance: int = None) -> bool:
        """API update helper modifying an existing record."""
        record = self.get(memory_id)
        if not record:
            return False
        
        cat = category if category is not None else record.category
        k = key if key is not None else record.key
        v = value if value is not None else record.value
        imp = importance if importance is not None else record.importance
        
        cat_clean = cat.strip().lower()
        if cat_clean not in self.CATEGORIES:
            cat_clean = "custom"
            
        return self.storage.update_record(memory_id, cat_clean, k.strip(), v.strip(), imp)

    def clear_all(self):
        """API clear_all helper wiping the memories database table."""
        self.storage.clear_all()

    def retrieve_context(self, query: str) -> str:
        """Retrieve relevant memories formatted as prompt context block."""
        all_memories = self.storage.get_all()
        relevant = self.retrieval.rank_and_select(query, all_memories)
        if not relevant:
            return ""
            
        lines = []
        for mem in relevant:
            lines.append(f"- [{mem.category.capitalize()}] {mem.key}: {mem.value} (ID: {mem.id})")
        return "\n[RECALLED LOCAL MEMORIES]\n" + "\n".join(lines) + "\n"
