# Shared dependencies: e.g., database sessions, auth functions
import bcrypt
from fastapi import Depends, HTTPException, status, Header
from app.database import get_supabase

async def get_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key missing. Please provide X-API-Key header."
        )

    # Query api_keys table in Supabase
    supabase = get_supabase()
    response = supabase.table("api_keys") \
        .select("id, key_hash, is_active, scopes") \
        .eq("is_active", True) \
        .execute()

    for row in response.data:
        if bcrypt.checkpw(x_api_key.encode(), row["key_hash"].encode()):
            return {"key_id": row["id"], "scopes": row["scopes"]}

    raise HTTPException(status_code=403, detail="Invalid or revoked API Key")