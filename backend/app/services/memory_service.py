"""
memory_service.py

Thin service wrapper around MemoryManager.
Routes call this — never storage or retrieval directly.
"""
from app.services.assistant_service import get_assistant
from app.memory.manager import MemoryManager


def get_memory() -> MemoryManager:
    """Return the shared MemoryManager from the active Summer instance."""
    return get_assistant().memory
