# Entry point: Creates FastAPI app, includes routers
from fastapi import FastAPI
from app.routers import recommendations

app = FastAPI(title="Recommendation Engine API")

app.include_router(recommendations.router, prefix="/routers")