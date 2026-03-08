# Schemas for recommendation output
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class RecommendationItem(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": 1,
            "name": "Wireless Headphones",
            "category": "electronics",
            "score": 85
        }
    })

    id: int
    name: str
    category: str
    score: int


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "success": True,
            "user_id": 123,
            "limit": 5,
            "recommendations": [
                {"id": 1, "name": "Wireless Headphones", "category": "electronics", "score": 85}
            ]
        }
    })

    success: bool
    user_id: Optional[int] = None
    limit: int
    recommendations: List[RecommendationItem]