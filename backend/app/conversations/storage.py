import sqlite3
import os
import datetime
import uuid
import json
from typing import List, Optional
from app.conversations.models import Conversation, Message


class ConversationStorage:

    def __init__(self, db_path: str):
        self.db_path = db_path
        db_dir = os.path.dirname(os.path.abspath(db_path))
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL DEFAULT 'New Chat',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    pinned INTEGER NOT NULL DEFAULT 0,
                    archived INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT NOT NULL DEFAULT '{}',
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def create(self, title: str = "New Chat") -> str:
        now = datetime.datetime.now().isoformat()
        conv_id = uuid.uuid4().hex
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversations (id, title, created_at, updated_at, pinned, archived) "
                "VALUES (?, ?, ?, ?, 0, 0)",
                (conv_id, title, now, now),
            )
            conn.commit()
            return conv_id

    def get(self, conversation_id: str) -> Optional[Conversation]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, created_at, updated_at, pinned, archived "
                "FROM conversations WHERE id = ?",
                (conversation_id,),
            )
            row = cursor.fetchone()
            if row:
                return Conversation(
                    id=row[0], title=row[1], created_at=row[2],
                    updated_at=row[3], pinned=bool(row[4]), archived=bool(row[5]),
                )
            return None

    def list(self) -> List[Conversation]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, created_at, updated_at, pinned, archived "
                "FROM conversations ORDER BY pinned DESC, updated_at DESC",
            )
            return [
                Conversation(
                    id=row[0], title=row[1], created_at=row[2],
                    updated_at=row[3], pinned=bool(row[4]), archived=bool(row[5]),
                )
                for row in cursor.fetchall()
            ]

    def update(self, conversation_id: str, **fields) -> bool:
        now = datetime.datetime.now().isoformat()
        valid = {"title", "pinned", "archived"}
        sets = []
        params = []
        for key, value in fields.items():
            if key not in valid:
                continue
            if key == "pinned" or key == "archived":
                value = int(bool(value))
            sets.append(f"{key} = ?")
            params.append(value)
        if not sets:
            return False
        sets.append("updated_at = ?")
        params.append(now)
        params.append(conversation_id)
        sql = f"UPDATE conversations SET {', '.join(sets)} WHERE id = ?"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, conversation_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM messages WHERE conversation_id = ?", (conversation_id,)
            )
            cursor.execute(
                "DELETE FROM conversations WHERE id = ?", (conversation_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def search(self, query: str) -> List[Conversation]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, created_at, updated_at, pinned, archived "
                "FROM conversations WHERE title LIKE ? ORDER BY pinned DESC, updated_at DESC",
                (f"%{query}%",),
            )
            return [
                Conversation(
                    id=row[0], title=row[1], created_at=row[2],
                    updated_at=row[3], pinned=bool(row[4]), archived=bool(row[5]),
                )
                for row in cursor.fetchall()
            ]

    def add_message(
        self, conversation_id: str, role: str, content: str,
        metadata: Optional[dict] = None,
    ) -> int:
        now = datetime.datetime.now().isoformat()
        meta_str = json.dumps(metadata) if metadata else "{}"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (conversation_id, role, content, timestamp, metadata) "
                "VALUES (?, ?, ?, ?, ?)",
                (conversation_id, role, content, now, meta_str),
            )
            cursor.execute(
                "UPDATE conversations SET updated_at = ? WHERE id = ?",
                (now, conversation_id),
            )
            conn.commit()
            return cursor.lastrowid

    def get_messages(self, conversation_id: str) -> List[Message]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, conversation_id, role, content, timestamp, metadata "
                "FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
                (conversation_id,),
            )
            return [
                Message(
                    id=row[0], conversation_id=row[1], role=row[2],
                    content=row[3], timestamp=row[4], metadata=row[5],
                )
                for row in cursor.fetchall()
            ]
