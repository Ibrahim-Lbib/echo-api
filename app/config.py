# Configuration: Env vars, database URLs (use os.environ for free)
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Settings():
    # API Keys
    API_KEYS: set[str] = {k for k in os.getenv("API_KEY_EXAMPLES", "").split(",") if k.strip()}
    APP_NAME: str = os.getenv("APP_NAME", "EchoAPI")

    # CORS (comma-separated origins, e.g. https://myapp.com,https://www.myapp.com)
    CORS_ORIGINS: list[str] = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]

    # Database Connection
    SB_URL: str = os.getenv("SUPABASE_URL")
    SB_KEY: str = os.getenv("SUPABASE_ANON_KEY")

    # Supabase PostgreSQL
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

settings = Settings()
