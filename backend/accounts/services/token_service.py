from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
class TokenService:
    def refresh_access_token(self, *, refresh_token: str) -> dict:
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            raise ValueError("Invalid or expired refresh token")
        
        access_token = str(refresh.access_token)

        new_refresh_token = str(refresh)

        return {
            "access_token":access_token,
            "refresh_token":new_refresh_token
        }
