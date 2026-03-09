# Shared dependencies: e.g., database sessions, auth functions
from fastapi import Depends, HTTPException, status, Header
from app.config import settings

async def get_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key missing. Please provide X-API-Key header."
        )

    if x_api_key not in settings.API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return x_api_key

async def verify_api_key(x_api_key: str = Header(...)):
    # query your Supabase api_keys table
    response = supabase.table("api_keys").select("*").eq("key", x_api_key).single().execute()
    if not response.data:
        raise HTTPException(status_code=403, detail={"success": False, "error": "Invalid API key", "status_code": 403})
    return response.data