"""
workspace_service.py

Thin service wrapper around WorkspaceManager.
Routes call this — never the workspace subsystem directly.
"""
from app.services.assistant_service import get_assistant
from app.workspace.manager import WorkspaceManager


def get_workspace() -> WorkspaceManager:
    """Return the shared WorkspaceManager from the active Summer instance."""
    return get_assistant().workspace
