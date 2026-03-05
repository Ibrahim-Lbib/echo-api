# Configuration: Env vars, database URLs (use os.environ for free)
import os

class Config():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False