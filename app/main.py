# Entry point: Creates FastAPI app, includes routers
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.utils.rate_limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routers import recommendations
from app.exceptions import http_exception_handler, general_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI(
    title="Recommendation Engine API",
    description=(
        "A scalable recommendation engine API.\n\n"
        "Features:\n"
        "- API Key authentication\n"
        "- Rate limiting\n"
        "- Personalized recommendations (DB + caching)\n"
        "- Ready for serverless deployment"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(recommendations.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Specify domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@limiter.limit("20/minute") # Root also protected
def root(request: Request):
    return {"message": "Welcome to the Recommendation Engine API"}