# Core router: Endpoints like /recommend/
from fastapi import APIRouter

router = APIRouter(
    prefix="/recommend", 
    tags=["recommendations"]
)

@router.get("/")
async def get_recommendations(user_id: int = None):
    return {"recommendations": ["item1", "item2", "item3"], "user_id": user_id}