"""
backend/main.py

FastAPI application entry point.

Run with:
    uvicorn main:app --reload

If you start Uvicorn from the repository root, use:
    uvicorn main:app --app-dir backend --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, chat, memory, workspace, models, conversations

app = FastAPI(
    title="Summer API",
    description="REST API for Project Summer — a local AI assistant.",
    version="0.1.0",
)

# Allow the Vite dev server (port 5173) to call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(models.router)
app.include_router(memory.router)
app.include_router(workspace.router)
app.include_router(conversations.router)
