# Core router: Endpoints like /recommend/
from fastapi import APIRouter, Depends, Request, Query
from app.dependencies import get_api_key
from app.utils.rate_limiter import limiter
from app.services.engine import get_recommendations as fetch_recommendations

router = APIRouter(
    prefix="/recommend", 
    tags=["recommendations"]
)

@router.get("/")
@limiter.limit("60/minute")
async def get_recommendations(
    request: Request,
    user_id: int | None = Query(None, description="Optional user ID for personalization"),
    limit: int = Query(5, ge=1, le=20, description="Number of recommendations (1-20)"),
    api_key: str = Depends(get_api_key)
):
    recs = await fetch_recommendations(user_id, limit)

    return {
        "success": True,
        "user_id": user_id,
        "limit": limit,
        "recommendations": [
            {"id": item["id"], "name": item["name"], "category": item["category"], "score": item["popularity"]}
            for item in recs
        ]
    }
    