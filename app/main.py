# Entry point: Creates FastAPI app, includes routers
from fastapi import FastAPI
from app.routers import recommendations

app = FastAPI(
    title="Recommendation Engine API",
    description="Scalable API for recommendations",
    version="1.0.0"
)

app.include_router(recommendations.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Recommendation Engine API"}