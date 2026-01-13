from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class AuthService:

    def login(self, *, email: str, password: str) -> dict:
        user = authenticate(email= email, password=password)
        if not user:
            raise ValueError("Invalid email or password")
        
        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
    
