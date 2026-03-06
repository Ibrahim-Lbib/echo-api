# Entry point: Creates FastAPI app, includes routers
from fastapi import FastAPI
from app.utils.rate_limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routers import recommendations


app = FastAPI(
    title="Recommendation Engine API",
    description="Scalable API for recommendations",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(recommendations.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Recommendation Engine API"}