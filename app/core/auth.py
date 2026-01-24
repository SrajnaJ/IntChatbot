from fastapi import Header, HTTPException
from app.core.config import INTERNAL_API_KEY


def verify_api_key(x_api_key: str = Header(...)):
    if INTERNAL_API_KEY is None:
        raise RuntimeError("INTERNAL_API_KEY not set")

    if x_api_key != INTERNAL_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
