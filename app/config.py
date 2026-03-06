# Configuration: Env vars, database URLs (use os.environ for free)
from dotenv import load_dotenv
import os

load_dotenv() 

class Settings():
    API_KEY_EXAMPLES: list[str] = os.getenv("API_KEY_EXAMPLES", "").split(",")
    APP_NAME: str = os.getenv("APP_NAME", "Recommendation Engine API")

    # Database
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

settings = Settings()
