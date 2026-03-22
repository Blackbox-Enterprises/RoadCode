"""Authentication — JWT tokens, session management, API keys."""
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass

@dataclass
class Session:
    user_id: str
    token: str
    created_at: float
    expires_at: float
    roles: list[str]

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

class AuthManager:
    """Handles authentication, token generation, and session management."""

    def __init__(self, secret: str | None = None) -> None:
        self.secret = secret or secrets.token_hex(32)
        self._sessions: dict[str, Session] = {}

    def create_session(self, user_id: str, roles: list[str] | None = None, ttl: int = 3600) -> Session:
        token = secrets.token_urlsafe(48)
        session = Session(
            user_id=user_id,
            token=token,
            created_at=time.time(),
            expires_at=time.time() + ttl,
            roles=roles or ["user"],
        )
        self._sessions[token] = session
        return session

    def validate(self, token: str) -> Session | None:
        session = self._sessions.get(token)
        if session and not session.is_expired:
            return session
        if session and session.is_expired:
            del self._sessions[token]
        return None

    def revoke(self, token: str) -> bool:
        return self._sessions.pop(token, None) is not None

    def hash_password(self, password: str) -> str:
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
        return f"{salt}:{hashed.hex()}"

    def verify_password(self, password: str, stored: str) -> bool:
        salt, hashed = stored.split(":")
        check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
        return hmac.compare_digest(check.hex(), hashed)
