import re
from typing import List
from app.memory.models import MemoryRecord

class MemoryRetrieval:
    """Determines which memories are relevant to include in the LLM system prompt context."""
    
    def __init__(self):
        pass

    def rank_and_select(self, query: str, memories: List[MemoryRecord]) -> List[MemoryRecord]:
        """Ranks memories by symbolic query relevance (word matches)."""
        query_words = set(re.findall(r"\w+", query.lower()))
        if not query_words:
            return []

        scored_memories = []
        for mem in memories:
            mem_words = set(re.findall(r"\w+", mem.content.lower()))
            overlap = len(query_words.intersection(mem_words))
            
            if mem.category.lower() in query_words:
                overlap += 2
                
            scored_memories.append((overlap, mem))
        
        # Sort memories descending by score
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        # Return top 5 relevant memories (only if score > 0)
        return [mem for score, mem in scored_memories if score > 0][:5]
