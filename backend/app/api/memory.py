from fastapi import APIRouter

router = APIRouter(prefix="/memory", tags=["Memory"])

# Memory endpoints will be implemented in a future step.
# GET    /memory           — list all memories
# POST   /memory           — store a new memory
# DELETE /memory/{id}      — forget by ID
# GET    /memory/search    — search memories
