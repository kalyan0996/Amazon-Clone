import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    """Shared JWT auth used across all microservices."""

    keyword = "Bearer"

    def authenticate(self, request):
        header = request.headers.get("Authorization")
        if not header or not header.startswith(self.keyword + " "):
            return None

        token = header.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        class SimpleUser:
            is_authenticated = True

            def __init__(self, claims):
                self.id = claims.get("sub")
                self.claims = claims

        return (SimpleUser(payload), token)
