from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Try to get token from Authorization header
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
            if raw_token is not None:
                try:
                    validated_token = self.get_validated_token(raw_token)
                    return (self.get_user(validated_token), validated_token)
                except Exception:
                    raise AuthenticationFailed("Invalid or expired token")
        
        # Fall back to cookie-based authentication
        raw_token = request.COOKIES.get("access_token")
        if raw_token is None:
            return None
        
        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")
        
        return (user, validated_token)