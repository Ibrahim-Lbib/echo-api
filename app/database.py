from supabase import create_client, Client 
from app.config import settings

# Lazy initialization
_supabase: Client | None = None

def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        url = settings.SUPABASE_URL
        key = settings.SUPABASE_ANON_KEY
        service_key = settings.SUPABASE_SERVICE_ROLE_KEY
        if not url or not key or not service_key:
            raise ValueError("Missing Supabase URL or SB_KEY in environment")
        _supabase = create_client(url, key, service_key)
    return _supabase