from ninja.security import HttpBearer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from jose import jwt, JWTError
from django.conf import settings

User = get_user_model()


class AuthBearer(HttpBearer):
    openapi_scheme_name = "Bearer Token"

    def authenticate(self, request, token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            username = payload.get('username')
            if username:
                user = get_object_or_404(User, username=username)
                return user
            return None
        except JWTError:
            return None