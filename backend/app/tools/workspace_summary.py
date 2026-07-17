from typing import Dict, Any
from app.tools.base import BaseTool
from app.workspace.manager import WorkspaceManager


class WorkspaceSummaryTool(BaseTool):
    """Allows Summer to summarize the current workspace project structure and metadata."""

    def __init__(self, workspace_manager: WorkspaceManager):
        self._workspace = workspace_manager

    @property
    def name(self) -> str:
        return "workspace_summary"

    @property
    def description(self) -> str:
        return (
            "Returns a structured summary of the current project workspace: "
            "project name, type, git status, file counts by extension, total size, "
            "and key entry-point files (README, config files, etc). "
            "Use this when the user asks about the project structure, stack, or wants "
            "to understand what this repository contains."
        )

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "refresh": {
                    "type": "boolean",
                    "description": "If true, re-scans the workspace before returning the summary. Defaults to false."
                }
            },
            "required": []
        }

    def execute(self, refresh: bool = False, **kwargs) -> Any:
        try:
            if refresh:
                self._workspace.refresh()
            return self._workspace.summary()
        except Exception as e:
            return f"Error: Failed to retrieve workspace summary. {str(e)}"
