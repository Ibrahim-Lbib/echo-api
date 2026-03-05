# Recommendation Engine API

A fast, scalable recommendation engine API built with [FastAPI](https://fastapi.tiangolo.com/).

## Technologies

- **FastAPI**: Modern, high-performance web framework for building APIs.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for interacting with the database.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Uvicorn**: ASGI web server implementation for Python.
- **Numpy**: Fundamental package for scientific computing with Python (used for recommendation algorithms).
- **Slowapi**: Rate limiting library for FastAPI.
- **Pytest**: Framework for writing simple and scalable tests.
- **Locust**: Load testing tool.
- **Docker**: For local development environment (Database, Redis).

## Project Structure

```
recommendation-api/
├── app/
│   ├── routers/       # API route definitions
│   ├── schemas/       # Pydantic schemas for data validation
│   ├── services/      # Business logic and recommendation engine core
│   ├── utils/         # Helper functions and utilities
│   ├── config.py      # Application configuration and environment variables
│   ├── dependencies.py# FastAPI dependency injection
│   └── main.py        # FastAPI application entry point
├── docs/              # Additional project documentation
├── tests/             # Pytest-based test suite
├── .env.example       # Example environment variables template
├── docker-compose.yml # Docker setup for local services (e.g., DB, Redis)
├── Dockerfile         # Dockerfile for building the application image
└── requirements.txt   # Python project dependencies
```

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ibrahim-Lbib/recommendation-api.git
cd recommendation-api
```

### 2. Set up environment variables

Copy the example `.env` file and update variables as needed.

```bash
cp .env.example .env
```

### 3. Start local services

Use Docker Compose to spin up the local development database and Redis.

```bash
docker-compose up -d
```

### 4. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

To run the application locally for development:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Once running, navigate to `http://localhost:8000/docs` in your browser to interact with the automatically generated Swagger UI API documentation.

## Testing

The project uses `pytest` for unit and integration testing.

To run the test suite:

```bash
pytest
```

To run load tests with `locust`:

```bash
locust -f tests/locustfile.py
```