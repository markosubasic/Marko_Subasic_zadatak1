import time
import httpx
import jwt

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from tickethub.core.config import get_settings 

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    payload = {"username": form.username, "password": form.password}

    if settings.bypass_dummy_auth:
        user = {"id": 1, "username": form.username}
    else:
        async with httpx.AsyncClient(base_url="https://dummyjson.com") as client:
            resp = await client.post("/auth/login", json=payload)
        if resp.status_code != 200:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Bad credentials")
        user = resp.json()

    token = jwt.encode(
        {"sub": user["id"], "username": user["username"], "iat": int(time.time())},
        settings.jwt_secret,
        algorithm="HS256",
    )
    return {"access_token": token, "token_type": "bearer"}
