from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class JWTAuthentication(JWTAuthentication):
    pass


class TokenAuthentication(TokenAuthentication):
    pass


class AccessToken(AccessToken):
    pass


class RefreshToken(RefreshToken):
    pass


class TokenObtainPairView(TokenObtainPairView):
    pass
