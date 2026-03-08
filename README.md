# EchoAPI

**EchoAPI** is a fast, scalable personalized recommendation engine built with [FastAPI](https://fastapi.tiangolo.com/), backed by **Supabase** for user preferences and **Upstash Redis** for lightning-fast cached responses.

## Technologies

| Library           | Purpose                                                                  |
| ----------------- | ------------------------------------------------------------------------ |
| **FastAPI**       | High-performance async web framework                                     |
| **Uvicorn**       | ASGI web server                                                          |
| **Pydantic**      | Data validation, schemas, and settings management                        |
| **python-dotenv** | Environment variable loading                                             |
| **Slowapi**       | Per-IP rate limiting (60 req/min on recommendations, 20 req/min on root) |
| **Supabase**      | Serverless Postgres DB — stores user preferences                         |
| **Upstash Redis** | Serverless Redis — caches recommendation results (TTL: 5 min)            |
| **cachetools**    | In-memory caching utilities                                              |
| **Pytest**        | Unit and integration testing                                             |

## Features

- 🔐 **API Key Authentication** — All endpoints protected via `X-API-Key` header
- ⚡ **Redis Caching** — Recommendations cached per `(user_id, limit)` pair for fast repeat requests
- 🎯 **Personalization** — Fetches `preferred_category` from Supabase and boosts matching items (+30 popularity)
- 🛡️ **Rate Limiting** — Built-in per-IP rate limiting using SlowAPI
- 🌐 **CORS Support** — Configured for cross-origin requests (tighten for production)
- 📋 **Background Tasks** — Non-blocking analytics logging after each recommendation response
- ⚠️ **Structured Error Handling** — Custom exception handlers return consistent JSON error responses
- 🐳 **Docker Ready** — Includes `Dockerfile` and `docker-compose.yml` for local development

## Project Structure

```
echo-api/
├── app/
│   ├── routers/
│   │   └── recommendations.py  # GET /recommend/ endpoint
│   ├── schemas/
│   │   └── recommeder.py       # Pydantic response models (RecommendationItem, RecommendationResponse)
│   ├── services/
│   │   └── engine.py           # Scoring logic, Supabase query, caching
│   ├── utils/
│   │   ├── rate_limiter.py     # SlowAPI limiter instance
│   │   └── cache.py            # Redis get/set helpers
│   ├── config.py               # App settings loaded from .env
│   ├── database.py             # Supabase client (lazy initialization)
│   ├── dependencies.py         # FastAPI API key dependency
│   ├── exceptions.py           # Global HTTP & unhandled exception handlers + logging config
│   ├── redis_client.py         # Upstash Redis client (lazy initialization)
│   └── main.py                 # App entry point, middleware, routers
├── docs/
├── tests/
│   └── test_recommendations.py
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Environment Variables

Create a `.env` file in the project root. Required variables:

```env
# API Authentication
API_KEY_EXAMPLES=supersecretkey123,testkey456

# App Info
APP_NAME=EchoAPI

# Supabase (get from supabase.com → Project Settings → API)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# Upstash Redis (get from upstash.com → Redis → REST API)
UPSTASH_REDIS_REST_URL=https://your-redis-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-redis-token
```

### Supabase Setup

1. Create a project at [supabase.com](https://supabase.com)
2. Go to **Table Editor → New Table** and create `user_preferences`:

| Column               | Type   | Notes                                |
| -------------------- | ------ | ------------------------------------ |
| `user_id`            | `int8` | Primary Key                          |
| `preferred_category` | `text` | e.g. `electronics`, `sports`, `home` |

3. Insert test data: `user_id = 123`, `preferred_category = electronics`

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ibrahim-Lbib/echo-api.git
cd echo-api
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
# Then fill in your Supabase and Upstash credentials
```

## Running the Application

### Local (without Docker)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### With Docker

```bash
docker build -t echo-api .
docker run -p 8000:8000 --env-file .env echo-api
```

### Local Dev with Docker Compose (Postgres + Redis)

The `docker-compose.yml` spins up a local Postgres and Redis instance, useful for development without Supabase/Upstash:

```bash
docker-compose up -d
```

Then open `http://localhost:8000/docs` for the interactive Swagger UI, or `http://localhost:8000/redoc` for ReDoc.

## API Endpoints

| Method | Endpoint      | Auth           | Description                      |
| ------ | ------------- | -------------- | -------------------------------- |
| `GET`  | `/`           | ❌             | Health check / welcome message   |
| `GET`  | `/recommend/` | ✅ `X-API-Key` | Get personalized recommendations |

### `GET /recommend/` Query Parameters

| Parameter | Type  | Default | Description                                                |
| --------- | ----- | ------- | ---------------------------------------------------------- |
| `user_id` | `int` | `None`  | Optional. Enables personalization via Supabase preferences |
| `limit`   | `int` | `5`     | Number of results to return (1–20)                         |

### Example Request

```bash
curl -H "X-API-Key: supersecretkey123" \
  "http://localhost:8000/recommend/?user_id=123&limit=5"
```

### Example Response

```json
{
  "success": true,
  "user_id": 123,
  "limit": 5,
  "recommendations": [
    { "id": 29, "name": "Laptop", "category": "electronics", "score": 129 },
    { "id": 15, "name": "Tablet", "category": "electronics", "score": 127 },
    { "id": 24, "name": "Smart Watch", "category": "electronics", "score": 125 }
  ]
}
```

### Error Responses

All errors return a consistent JSON shape:

```json
{
  "success": false,
  "error": "API Key missing. Please provide X-API-Key header.",
  "status_code": 401
}
```

| Status Code | Meaning                                      |
| ----------- | -------------------------------------------- |
| `401`       | Missing `X-API-Key` header                   |
| `403`       | Invalid API key                              |
| `422`       | Validation error (e.g. `limit` out of range) |
| `429`       | Rate limit exceeded                          |
| `500`       | Internal server error                        |

## Deployment

EchoAPI is designed to be easily deployable on container-based platforms like **Railway**, **Render**, or **Fly.io**.

### Automated Deployment (Railway)

1. **Connect your GitHub Repo**: Point Railway to your `echo-api` repository.
2. **Environment Variables**: Configure the following in the Railway dashboard:
   - `SUPABASE_URL` & `SUPABASE_ANON_KEY`
   - `UPSTASH_REDIS_REST_URL` & `UPSTASH_REDIS_REST_TOKEN`
   - `API_KEY_EXAMPLES` (comma-separated keys)
   - `CORS_ORIGINS`: Set this to your frontend domain (e.g., `https://myapp.com`) or `*` to allow all.
3. **Deploy**: Railway will automatically detect the `Dockerfile` and `railway.toml` to build and start the service.

### Manual Docker Deployment

```bash
# Build the production image
docker build -t echo-api .

# Run with environment variables
docker run -p 8000:8000 \
  -e SUPABASE_URL=... \
  -e SUPABASE_ANON_KEY=... \
  -e UPSTASH_REDIS_REST_URL=... \
  -e UPSTASH_REDIS_REST_TOKEN=... \
  -e API_KEY_EXAMPLES=... \
  echo-api
```

### Health Checks

The app provides a `/health` endpoint for monitoring and liveness checks:
- **URL**: `GET /health`
- **Response**: `{"status": "ok"}`
- **Note**: This endpoint does not require an API key or rate limiting.

## Testing

```bash
pytest
```

Tests use dependency overrides to bypass auth and mock the Redis cache, so no live credentials are needed.
