from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ecommerce.core.logging import get_logger

logger = get_logger(__name__)

class AuthService:

    def login(self, *, email: str, password: str) -> dict:
        logger.info("login_attempt", email_domain=email.split('@')[1])
        user = authenticate(email= email, password=password)
        if not user:
            logger.warning("login_failed", email_domain=email.split('@')[1], reason="Invalid credentials")
            raise ValueError("Invalid email or password")
        try:
            refresh = RefreshToken.for_user(user)
            logger.info(
                "login_successful",
                user_id=user.id,
                email_domain=email.split('@')[1],
            )

            return {
                "user": user,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }
        except Exception as e:
            logger.error(
                "token_generation_failed",
                user_id=user.id,
                error=str(e),
                exc_info=True
            )
            raise
    
