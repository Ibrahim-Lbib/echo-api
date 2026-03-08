# e.g., schemas for user input and recommendation output
from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendationItem(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Wireless Headphones")
    category: str = Field(..., example="electronics")
    score: int = Field(..., example=85)

class RecommendationResponse(BaseModel):
    success: bool = Field(..., example=True)
    user_id: Optional[int] = Field(None, example=123)
    limit: int = Field(..., example=5)
    recommendations: List[RecommendationItem]