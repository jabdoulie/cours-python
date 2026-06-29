"""
02_auth/jwt_server.py
──────────────────────
FastAPI server with JWT authentication.

Flow:
  1. POST /auth/token  { username, password }  →  { access_token, token_type }
  2. Use Bearer token in Authorization header for protected routes.

Run:
    uvicorn jwt_server:app --reload --port 8002

Test:
    # Get a token
    curl -X POST http://localhost:8002/auth/token \
         -H "Content-Type: application/json" \
         -d '{"username": "alice", "password": "password123"}'

    # Use the token
    curl -H "Authorization: Bearer <token>" http://localhost:8002/me

    # Or use the test client:
    python client.py --mode jwt
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="JWT Auth Demo")

# ─── Config ───────────────────────────────────────────────────────────────────

SECRET_KEY = "super-secret-do-not-commit-me"   # In prod: load from env var
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fake user database — in prod this would be a real DB with hashed passwords
FAKE_USERS = {
    "alice": {"username": "alice", "password": "password123", "role": "admin"},
    "bob":   {"username": "bob",   "password": "hunter2",    "role": "viewer"},
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ─── Models ───────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60


class UserInfo(BaseModel):
    username: str
    role: str


# ─── Helpers ──────────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    payload["exp"] = expire
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and verify a JWT. Raises HTTPException on failure."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ─── Dependencies ─────────────────────────────────────────────────────────────

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInfo:
    payload = decode_token(token)
    username = payload.get("sub")
    if username is None or username not in FAKE_USERS:
        raise HTTPException(status_code=401, detail="User not found")
    user = FAKE_USERS[username]
    return UserInfo(username=user["username"], role=user["role"])


def require_admin(user: Annotated[UserInfo, Depends(get_current_user)]) -> UserInfo:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return user


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.post("/auth/token", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """Exchange username + password for a JWT access token."""
    user = FAKE_USERS.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    logger.info("Token issued for user: %s", user["username"])
    return TokenResponse(access_token=token)


@app.get("/me", response_model=UserInfo)
async def get_me(user: Annotated[UserInfo, Depends(get_current_user)]):
    """Return info about the currently authenticated user."""
    return user


@app.get("/admin/dashboard")
async def admin_dashboard(user: Annotated[UserInfo, Depends(require_admin)]):
    """Admin-only endpoint. Returns 403 for non-admins."""
    return {"message": f"Welcome, {user.username}! This is the admin dashboard."}


@app.get("/health")
async def health():
    return {"status": "ok"}
