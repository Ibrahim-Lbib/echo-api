# Recommendation Engine API

A fast, scalable personalized recommendation engine built with [FastAPI](https://fastapi.tiangolo.com/), backed by **Supabase** for user preferences and **Upstash Redis** for lightning-fast cached responses.

## Technologies

| Library | Purpose |
|---|---|
| **FastAPI** | High-performance async web framework |
| **Uvicorn** | ASGI web server |
| **Pydantic** | Data validation and settings management |
| **python-dotenv** | Environment variable loading |
| **Slowapi** | Per-IP rate limiting (60 req/min on recommendations, 20 req/min on root) |
| **Supabase** | Serverless Postgres DB — stores user preferences |
| **Upstash Redis** | Serverless Redis — caches recommendation results (TTL: 5 min) |
| **cachetools** | In-memory caching utilities |
| **Pytest** | Unit and integration testing |

## Features

- 🔐 **API Key Authentication** — All endpoints protected via `X-API-Key` header
- ⚡ **Redis Caching** — Recommendations cached per `(user_id, limit)` pair for fast repeat requests
- 🎯 **Personalization** — Fetches `preferred_category` from Supabase and boosts matching items (+30 popularity)
- 🛡️ **Rate Limiting** — Built-in per-IP rate limiting using SlowAPI
- 🌐 **CORS Support** — Configured for cross-origin requests (tighten for production)
- 📋 **Background Tasks** — Non-blocking analytics logging after each recommendation response

## Project Structure

```
recommendation-api/
├── app/
│   ├── routers/
│   │   └── recommendations.py  # GET /recommend/ endpoint
│   ├── services/
│   │   └── engine.py           # Scoring logic, Supabase query, caching
│   ├── utils/
│   │   ├── rate_limiter.py     # SlowAPI limiter instance
│   │   └── cache.py            # Redis get/set helpers
│   ├── config.py               # App settings loaded from .env
│   ├── database.py             # Supabase client (lazy initialization)
│   ├── redis_client.py         # Upstash Redis client (lazy initialization)
│   ├── dependencies.py         # FastAPI API key dependency
│   └── main.py                 # App entry point, middleware, routers
├── docs/
├── tests/
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
APP_NAME=Recommendation Engine API

# Supabase (get from supabase.com → Project Settings → API)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# Upstash Redis (get from upstash.com → Redis → REST API)
UPSTASH_REDIS_REST_URL=https://your-redis-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-redis-token

# Supabase PostgreSQL (optional, for SQLAlchemy ORM integration)
DATABASE_URL=postgresql://user:password@host:port/postgres
```

### Supabase Setup

1. Create a project at [supabase.com](https://supabase.com)
2. Go to **Table Editor → New Table** and create `user_preferences`:

| Column | Type | Notes |
|---|---|---|
| `user_id` | `int8` | Primary Key |
| `preferred_category` | `text` | e.g. `electronics`, `sports`, `home` |

3. Insert test data: `user_id = 123`, `preferred_category = electronics`

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ibrahim-Lbib/recommendation-api.git
cd recommendation-api
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

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000/docs` for the interactive Swagger UI.

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/` | ❌ | Health check / welcome message |
| `GET` | `/recommend/` | ✅ `X-API-Key` | Get personalized recommendations |

### `GET /recommend/` Query Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_id` | `int` | `None` | Optional. Enables personalization via Supabase preferences |
| `limit` | `int` | `5` | Number of results to return (1–20) |

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
    {"id": 15, "name": "Tablet", "category": "electronics", "score": 97},
    {"id": 29, "name": "Laptop", "category": "electronics", "score": 99},
    {"id": 24, "name": "Smart Watch", "category": "electronics", "score": 95}
  ]
}
```

## Testing

```bash
pytest
```