import sqlite3
import os
import datetime
from typing import List
from app.memory.models import MemoryRecord

class MemoryStorage:
    """Handles raw SQLite CRUD queries for stored memories using a key-value categorized schema."""
    
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
                    category TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    importance INTEGER DEFAULT 3,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(category, key) ON CONFLICT REPLACE
                )
            """)
            conn.commit()

    def insert_or_update(self, category: str, key: str, value: str, importance: int = 3) -> int:
        """Insert or replace a memory record and return its row ID."""
        now = datetime.datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, created_at FROM memories WHERE category = ? AND key = ?",
                (category, key)
            )
            row = cursor.fetchone()
            
            if row:
                row_id, created_at = row
                cursor.execute(
                    "UPDATE memories SET value = ?, importance = ?, updated_at = ? WHERE id = ?",
                    (value, importance, now, row_id)
                )
                conn.commit()
                return row_id
            else:
                cursor.execute(
                    "INSERT INTO memories (category, key, value, importance, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (category, key, value, importance, now, now)
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
            cursor.execute("SELECT id, category, key, value, importance, created_at, updated_at FROM memories ORDER BY id DESC")
            rows = cursor.fetchall()
            return [MemoryRecord(*row) for row in rows]

    def search(self, query: str) -> List[MemoryRecord]:
        """Search memories matching keywords in key or value."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, category, key, value, importance, created_at, updated_at FROM memories "
                "WHERE key LIKE ? OR value LIKE ? ORDER BY id DESC",
                (f"%{query}%", f"%{query}%")
            )
            rows = cursor.fetchall()
            return [MemoryRecord(*row) for row in rows]

    def get_by_id(self, memory_id: int) -> MemoryRecord:
        """Fetch a specific memory record by its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, category, key, value, importance, created_at, updated_at FROM memories WHERE id = ?",
                (memory_id,)
            )
            row = cursor.fetchone()
            return MemoryRecord(*row) if row else None

    def update_record(self, memory_id: int, category: str, key: str, value: str, importance: int) -> bool:
        """Update fields of an existing memory record."""
        now = datetime.datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE memories SET category = ?, key = ?, value = ?, importance = ?, updated_at = ? WHERE id = ?",
                (category, key, value, importance, now, memory_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_by_category(self, category: str) -> bool:
        """Delete memories matching a category."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE category = ?", (category,))
            conn.commit()
            return cursor.rowcount > 0

    def delete_by_key(self, key: str) -> bool:
        """Delete memories matching a key."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE key = ?", (key,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all(self):
        """Wipe all memory records."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM memories")
            conn.commit()
