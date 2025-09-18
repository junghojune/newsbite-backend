import base64
import hmac
import time
from hashlib import sha256
from typing import Optional, Tuple


def _b64u_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64u_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def generate_token(email: str, purpose: str, secret: str, ttl_hours: int = 48) -> str:
    email = email.strip().lower()
    issued_ts = int(time.time())
    payload = f"{email}|{purpose}|{issued_ts}".encode("utf-8")
    sig = hmac.new(secret.encode("utf-8"), payload, sha256).digest()
    return f"{_b64u_encode(payload)}.{_b64u_encode(sig)}"


def verify_token(token: str, purpose: str, secret: str, ttl_hours: int = 48) -> Tuple[bool, Optional[str]]:
    try:
        payload_b64, sig_b64 = token.split(".")
        payload = _b64u_decode(payload_b64)
        expected_sig = _b64u_decode(sig_b64)
        computed_sig = hmac.new(secret.encode("utf-8"), payload, sha256).digest()
        if not hmac.compare_digest(expected_sig, computed_sig):
            return False, None
        payload_str = payload.decode("utf-8")
        email, token_purpose, issued_ts_str = payload_str.split("|")
        if token_purpose != purpose:
            return False, None
        issued_ts = int(issued_ts_str)
        if time.time() - issued_ts > ttl_hours * 3600:
            return False, None
        return True, email
    except Exception:
        return False, None

