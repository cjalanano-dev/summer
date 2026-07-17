from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.assistant_service import get_assistant

router = APIRouter(prefix="/models", tags=["Models"])


class ModelSelectRequest(BaseModel):
    model: str


@router.get("")
def list_models():
    assistant = get_assistant()
    models = assistant.llm_client.get_installed_models()
    current_model = assistant.config.model_name

    if current_model and current_model not in models:
        models = [current_model, *models]

    return {
        "currentModel": current_model,
        "models": models,
    }


@router.post("/select")
def select_model(request: ModelSelectRequest):
    assistant = get_assistant()
    model_name = request.model.strip()

    if not model_name:
        raise HTTPException(status_code=400, detail="Model name is required.")

    assistant.config.model_name = model_name
    return {"currentModel": assistant.config.model_name}