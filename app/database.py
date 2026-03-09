from supabase import create_client, Client 
from app.config import settings

# Lazy initialization
_supabase: Client | None = None

def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        url = settings.SB_URL
        key = settings.SB_KEY

        url_2 = settings.SUPABASE_URL_2
        key_2 = settings.SUPABASE_SERVICE_ROLE_KEY  

        if not url or not key or not url_2 or not key_2:
            raise ValueError("Missing Supabase URL or SB_KEY in environment")
        _supabase = create_client(url, key, url_2, key_2)
    return _supabase