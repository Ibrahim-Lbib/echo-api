# Entry point: Creates FastAPI app, includes routers
from fastapi import FastAPI
from app.api.v1 import endpoints

app = FastAPI(title="Recommendation Engine API")

app.include_router(endpoints.router, prefix="/api/v1")