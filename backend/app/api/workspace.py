from fastapi import APIRouter

router = APIRouter(prefix="/workspace", tags=["Workspace"])

# Workspace endpoints will be implemented in a future step.
# GET /workspace/summary  — return the current project workspace summary
# GET /workspace/files    — list workspace files
# POST /workspace/refresh — re-scan the workspace
