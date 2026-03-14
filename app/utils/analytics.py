import logging
from datetime import datetime
import json
from fastapi import Request

# Extend existing logger
logger = logging.getLogger(__name__)

def log_request(request: Request, response_status: int, user_id: str | None = None, duration_ms: float | None = None):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host,
        "user_id": user_id,
        "status": response_status,
        "duration_ms": duration_ms,
        "api_key": request.headers.get("X-API-Key", "unknown")[:8] + "..."  # Partial for privacy
    }
    logger.info(json.dumps(log_entry))
    # Optional: append to file for persistence
    with open("api_logs.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")