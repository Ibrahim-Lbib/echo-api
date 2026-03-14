from fastapi import APIRouter, BackgroundTasks
from app.services.precompute import precompute_popular_recommendations

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/precompute")
def trigger_precompute(background_tasks: BackgroundTasks):
    background_tasks.add_task(precompute_popular_recommendations)
    return {"status": "Precomputation started in background"}