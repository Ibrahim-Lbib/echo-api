from supabase import create_client, Client 
from app.config import settings

# Lazy initialization
_supabase: Client | None = None

def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        url = settings.SB_URL
        key = settings.SB_KEY
        if not url or not key:
            raise ValueError("Missing Supabase URL or SB_KEY in environment")
        _supabase = create_client(url, key)
    return _supabase

def get_supabase_2() -> Client:
    url = settings.SUPABASE_URL_2
    key = settings.SUPABASE_SERVICE_ROLE_KEY
    if not url or not key:
        raise ValueError("Missing Supabase URL or SB_KEY in environment")
    return create_client(url, key)