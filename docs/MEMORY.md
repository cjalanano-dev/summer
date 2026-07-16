# Project Summer Memory Design

This document describes the design specifications of Summer's memory system.

## Design Principles

1. **Local-First Privacy**:
   All conversation histories, parameters, preferences, and facts remain local on the user's computer.
2. **Decoupled Lifecycle**:
   - Short-term context: Tracked dynamically in the active session (`Conversation` in `app/conversation.py`).
   - Long-term memory (Future): Handled by a database manager module using SQLite or a local vector index.

## SQLite Long-Term Memory (Planned Schema)

```sql
CREATE TABLE IF NOT EXISTS user_preferences (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS memory_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT, -- e.g., projects, goals, routines
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Retrieval

Prior to executing a loop iteration, the `Planner` will load relevant facts from the database and insert them into the system prompt context, keeping memory updates isolated from the CLI and core agent logic.
