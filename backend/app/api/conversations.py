import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.conversations.service import get_conversation_manager

router = APIRouter(prefix="/conversations", tags=["Conversations"])


class CreateConversationRequest(BaseModel):
    title: str = "New Chat"


class UpdateConversationRequest(BaseModel):
    title: Optional[str] = None
    pinned: Optional[bool] = None
    archived: Optional[bool] = None


class AddMessageRequest(BaseModel):
    role: str
    content: str
    metadata: Optional[dict] = None


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    pinned: bool
    archived: bool


class MessageResponse(BaseModel):
    id: int
    conversation_id: str
    role: str
    content: str
    timestamp: str
    metadata: dict


@router.get("")
def list_conversations():
    manager = get_conversation_manager()
    conversations = manager.list()
    return [
        ConversationResponse(
            id=c.id, title=c.title, created_at=c.created_at,
            updated_at=c.updated_at, pinned=c.pinned, archived=c.archived,
        )
        for c in conversations
    ]


@router.post("")
def create_conversation(request: CreateConversationRequest):
    manager = get_conversation_manager()
    conv = manager.create(request.title)
    return ConversationResponse(
        id=conv.id, title=conv.title, created_at=conv.created_at,
        updated_at=conv.updated_at, pinned=conv.pinned, archived=conv.archived,
    )


@router.get("/{conversation_id}")
def get_conversation(conversation_id: str):
    manager = get_conversation_manager()
    conv = manager.load(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationResponse(
        id=conv.id, title=conv.title, created_at=conv.created_at,
        updated_at=conv.updated_at, pinned=conv.pinned, archived=conv.archived,
    )


@router.patch("/{conversation_id}")
def update_conversation(conversation_id: str, request: UpdateConversationRequest):
    manager = get_conversation_manager()
    if not manager.load(conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")

    manager.save(
        conversation_id,
        title=request.title,
        pinned=request.pinned,
        archived=request.archived,
    )

    conv = manager.load(conversation_id)
    return ConversationResponse(
        id=conv.id, title=conv.title, created_at=conv.created_at,
        updated_at=conv.updated_at, pinned=conv.pinned, archived=conv.archived,
    )


@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: str):
    manager = get_conversation_manager()
    if not manager.load(conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    manager.delete(conversation_id)
    return {"success": True}


@router.get("/search/{query}")
def search_conversations(query: str):
    manager = get_conversation_manager()
    conversations = manager.search(query)
    return [
        ConversationResponse(
            id=c.id, title=c.title, created_at=c.created_at,
            updated_at=c.updated_at, pinned=c.pinned, archived=c.archived,
        )
        for c in conversations
    ]


@router.post("/{conversation_id}/messages")
def add_message(conversation_id: str, request: AddMessageRequest):
    manager = get_conversation_manager()
    if not manager.load(conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    msg = manager.add_message(
        conversation_id, request.role, request.content,
        metadata=request.metadata,
    )
    return MessageResponse(
        id=msg.id, conversation_id=msg.conversation_id, role=msg.role,
        content=msg.content, timestamp=msg.timestamp,
        metadata=json.loads(msg.metadata),
    )


@router.get("/{conversation_id}/messages")
def get_messages(conversation_id: str):
    manager = get_conversation_manager()
    if not manager.load(conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = manager.get_messages(conversation_id)
    return [
        MessageResponse(
            id=m.id, conversation_id=m.conversation_id, role=m.role,
            content=m.content, timestamp=m.timestamp,
            metadata=json.loads(m.metadata),
        )
        for m in messages
    ]
