# Core router: Endpoints like /recommend/
from fastapi import APIRouter

router = APIRouter(prefix="/recommend", tags=["recommendations"])

@router.get("/")
async def get_recommendations(user_id: int):
    return [
        {"id": 1, "name": "Item A", "score": 0.92},
        {"id": 2, "name": "Item B", "score": 0.87},
        {"id": 3, "name": "Item C", "score": 0.79},
    ]