from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json

from app.services.assistant_service import get_assistant

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    model: Optional[str] = None


@router.post("")
def chat(request: ChatRequest):
    assistant = get_assistant()

    def event_generator():
        try:
            generator = assistant.chat(
                prompt=request.message,
                model=request.model,
                conversation_id=request.conversation_id,
            )
            for chunk_type, text in generator:
                if chunk_type == "content":
                    yield f"data: {json.dumps({'content': text})}\n\n"
                elif chunk_type == "thinking":
                    yield f"data: {json.dumps({'content': f'<think>{text}</think>'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
