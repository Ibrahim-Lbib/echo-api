import bcrypt
import uuid

def create_api_key(user_id: int, scopes: list = ["read"]):
    raw_key = f"rec_{uuid.uuid4().hex[:24]}"  # Human-readable prefix
    hashed = bcrypt.hashpw(raw_key.encode(), bcrypt.gensalt())
    supabase = get_supabase()
    supabase.table("api_keys").insert({
        "key_hash": hashed.decode(),
        "user_id": user_id,
        "scopes": scopes
    }).execute()
    return raw_key  # Show once!