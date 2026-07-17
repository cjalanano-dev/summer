import re
from typing import List
from app.memory.models import MemoryRecord

class MemoryRetrieval:
    """Determines which memories are relevant to include in the LLM system prompt context."""
    
    def __init__(self):
        pass

    def rank_and_select(self, query: str, memories: List[MemoryRecord]) -> List[MemoryRecord]:
        """Ranks and filters memories incorporating project context, top preferences, top goals, and keyword overlaps."""
        # 1. Gather all 'project' memories
        projects = [m for m in memories if m.category == "project"]
        
        # 2. Gather top 5 'preference' memories sorted by importance desc
        preferences = sorted(
            [m for m in memories if m.category == "preference"],
            key=lambda x: x.importance,
            reverse=True
        )[:5]
        
        # 3. Gather top 5 'goal' memories sorted by importance desc
        goals = sorted(
            [m for m in memories if m.category == "goal"],
            key=lambda x: x.importance,
            reverse=True
        )[:5]
        
        # 4. Keyword matches for other category records
        included_ids = {m.id for m in projects + preferences + goals}
        query_words = set(re.findall(r"\w+", query.lower()))
        keyword_matches = []
        
        if query_words:
            for mem in memories:
                if mem.id in included_ids:
                    continue
                # Tokenize key and value
                key_words = set(re.findall(r"\w+", mem.key.lower()))
                val_words = set(re.findall(r"\w+", mem.value.lower()))
                combined = key_words.union(val_words)
                
                if query_words.intersection(combined):
                    keyword_matches.append(mem)
                    
        # Return merged list
        return list(projects) + list(preferences) + list(goals) + keyword_matches
