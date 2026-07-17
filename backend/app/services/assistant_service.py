"""
assistant_service.py

Thin service wrapper around the Summer coordinator.
Routes and API handlers call this — never the assistant directly.
"""
from __future__ import annotations

from app.assistant import Summer

# Module-level singleton — instantiated once on first use
_instance: Summer | None = None


def get_assistant() -> Summer:
    """Return the shared Summer instance, creating it if needed."""
    global _instance
    if _instance is None:
        _instance = Summer()
    return _instance
