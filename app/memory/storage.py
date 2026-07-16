import sqlite3
import os
import datetime
from typing import List
from app.memory.models import MemoryRecord

class MemoryStorage:
    """Handles raw SQLite CRUD queries for stored memories."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        db_dir = os.path.dirname(os.path.abspath(db_path))
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def insert(self, category: str, content: str) -> int:
        """Insert a memory and return its primary key ID."""
        created_at = datetime.datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO memories (category, content, created_at) VALUES (?, ?, ?)",
                (category, content, created_at)
            )
            conn.commit()
            return cursor.lastrowid

    def delete(self, memory_id: int) -> bool:
        """Delete a memory by its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_all(self) -> List[MemoryRecord]:
        """Fetch all stored memories."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, category, content, created_at FROM memories ORDER BY id DESC")
            rows = cursor.fetchall()
            return [MemoryRecord(*row) for row in rows]

    def search(self, query: str) -> List[MemoryRecord]:
        """Search memories via SQL LIKE keyword match."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, category, content, created_at FROM memories WHERE content LIKE ? ORDER BY id DESC",
                (f"%{query}%",)
            )
            rows = cursor.fetchall()
            return [MemoryRecord(*row) for row in rows]
