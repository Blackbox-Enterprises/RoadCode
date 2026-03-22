"""Crypto utilities — hashing, signing, chain verification."""
import hashlib
import hmac
import secrets
from typing import Optional

def sha256(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()

def chain_hash(current: str, previous: Optional[str] = None) -> str:
    payload = f"{previous or 'genesis'}:{current}"
    return sha256(payload)

def hmac_sign(message: str, key: str) -> str:
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def hmac_verify(message: str, key: str, signature: str) -> bool:
    expected = hmac_sign(message, key)
    return hmac.compare_digest(expected, signature)

def generate_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)

def generate_id(prefix: str = "") -> str:
    token = secrets.token_hex(8)
    return f"{prefix}-{token}" if prefix else token
