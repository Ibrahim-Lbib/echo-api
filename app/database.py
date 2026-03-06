from supabase import create_client, Client 
from app.config import settings
import os

# Lazy initialization
_supabase: Client | None = None

def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        url = settings.SUPABASE_URL
        key = settings.SUPABASE_ANON_KEY
        if not url or not key:
            raise ValueError("Missing Supabase URL or ANON_KEY in environment")
        _supabase = create_client(url, key)
    return _supabase