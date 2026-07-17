from app.conversations.manager import ConversationManager
from app.services.assistant_service import get_assistant


def get_conversation_manager() -> ConversationManager:
    return get_assistant().conversation_manager
