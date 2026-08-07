import jwt
from datetime import datetime, timezone
from django.conf import settings


def _make_token(user, token_type: str, ttl):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "type": token_type,
        "iat": now,
        "exp": now + ttl,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def create_access_token(user):
    return _make_token(user, "access", settings.JWT_ACCESS_TTL)


def create_refresh_token(user):
    return _make_token(user, "refresh", settings.JWT_REFRESH_TTL)


def decode_refresh_token(token: str):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    if payload.get("type") != "refresh":
        raise jwt.InvalidTokenError("Not a refresh token")
    return payload
