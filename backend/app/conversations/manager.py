from typing import List, Optional
from app.conversations.storage import ConversationStorage
from app.conversations.models import Conversation, Message


class ConversationManager:

    def __init__(self, db_path: str):
        self.storage = ConversationStorage(db_path)

    def create(self, title: str = "New Chat") -> Conversation:
        conv_id = self.storage.create(title)
        return self.load(conv_id)

    def load(self, conversation_id: str) -> Optional[Conversation]:
        return self.storage.get(conversation_id)

    def save(
        self,
        conversation_id: str,
        title: Optional[str] = None,
        pinned: Optional[bool] = None,
        archived: Optional[bool] = None,
    ) -> bool:
        fields = {}
        if title is not None:
            fields["title"] = title
        if pinned is not None:
            fields["pinned"] = pinned
        if archived is not None:
            fields["archived"] = archived
        if not fields:
            return False
        return self.storage.update(conversation_id, **fields)

    def rename(self, conversation_id: str, title: str) -> bool:
        return self.save(conversation_id, title=title)

    def pin(self, conversation_id: str, value: bool = True) -> bool:
        return self.save(conversation_id, pinned=value)

    def archive(self, conversation_id: str, value: bool = True) -> bool:
        return self.save(conversation_id, archived=value)

    def delete(self, conversation_id: str) -> bool:
        return self.storage.delete(conversation_id)

    def list(self) -> List[Conversation]:
        return self.storage.list()

    def search(self, query: str) -> List[Conversation]:
        return self.storage.search(query)

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> Message:
        self.storage.add_message(conversation_id, role, content, metadata=metadata)
        messages = self.storage.get_messages(conversation_id)
        return messages[-1]

    def get_messages(self, conversation_id: str) -> List[Message]:
        return self.storage.get_messages(conversation_id)
