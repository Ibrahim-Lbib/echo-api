# Entry point: Creates FastAPI app, includes routers
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.utils.rate_limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routers import recommendations


app = FastAPI(
    title="Recommendation Engine API",
    description="Scalable API for recommendations",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Specify domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(recommendations.router)

@app.get("/")
@limiter.limit("20/minute") # Root also protected
def root(request: Request):
    return {"message": "Welcome to the Recommendation Engine API"}