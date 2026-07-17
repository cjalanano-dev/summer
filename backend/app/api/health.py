from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["System"])


@router.get("")
def health():
    """Health check — confirms the API is reachable."""
    return {"status": "ok", "service": "summer-api"}
