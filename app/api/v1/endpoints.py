from fastapi import APIRouter

router = APIRouter()

@router.get("/recommend")
async def recommend():
    return [
        {"id": 1, "name": "Item A", "score": 0.92},
        {"id": 2, "name": "Item B", "score": 0.87},
        {"id": 3, "name": "Item C", "score": 0.79},
    ]