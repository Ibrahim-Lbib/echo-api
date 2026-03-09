from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_api_key
from app.schemas.recommeder import PreferenceCreate, PreferenceResponse
from app.main import limiter
from fastapi import Request
from app.database import get_supabase

router = APIRouter(
    prefix="/preferences",
    tags=["preferences"]
)

@router.post(
    "/",
    response_model=PreferenceResponse,
    summary="Update or set user preferred category",
    description="Creates or updates the preferred category for a given user_id."
)
@limiter.limit("30/minute")  # Lower limit since this is write operation
async def update_preference(
    request: Request,
    preference: PreferenceCreate,
    api_key: str = Depends(get_api_key)
):
    try:
        # Upsert (update if exists, insert if not)
        supabase = get_supabase()
        response = supabase.table("user_preferences").upsert({
            "user_id": preference.user_id,
            "preferred_category": preference.preferred_category,
            "updated_at": "now()"
        }).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to update preference")
        
        return PreferenceResponse(
            success=True,
            message="Preference updated successfully",
            user_id=preference.user_id,
            preferred_category=preference.preferred_category
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")