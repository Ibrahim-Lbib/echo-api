# Shared dependencies: e.g., database sessions, auth functions
from fastapi import Depends, HTTPException, status, Header
from app.config import settings
from supabase import create_client

async def get_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key missing. Please provide X-API-Key header."
        )

    # Query api_keys table in Supabase
    supabase_auth = create_client(settings.SUPABASE_URL_2, settings.SUPABASE_SERVICE_ROLE_KEY)
    response = supabase_auth.table("api_keys").select("*").eq("key", x_api_key).execute()

    if not response.data or len(response.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"success": False, "error": "Invalid API key", "status_code": 403}
        )

    return response.data[0]