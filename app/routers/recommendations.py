# Core router: Endpoints like /recommend/
from fastapi import APIRouter, Depends, Request
from app.dependencies import get_api_key
from app.utils.rate_limiter import limiter

router = APIRouter(
    prefix="/recommend", 
    tags=["recommendations"]
)

@router.get("/")
@limiter.limit("5/minute")
async def get_recommendations(
    request: Request,
    user_id: int | None = None,
    api_key: str = Depends(get_api_key)
):
    return {
        "message": "Succes - rate limited & authenticated",
        "user_id": user_id,
        "recommendations": ["item1", "item2", "item3"], 
    }