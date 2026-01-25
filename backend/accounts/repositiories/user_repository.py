from accounts.models import User
from ecommerce.core.logging import get_logger
from django.db import DatabaseError

logger = get_logger(__name__)

class UserRepository:
    def get_by_email(self, email: str) -> User | None:
        try:
            user = User.objects.filter(email=email).first()
            if user:
                logger.debug(
                    "user_found_by_email",
                    user_id=user.id,
                    email_domain=email.split('@')[1]
                )
            else:
                logger.debug("user_not_found_by_email", email_domain=email.split('@')[1])
            return user
        
        except DatabaseError as e:
            logger.error(
                "database_error_fetching_user",
                error=str(e),
                email_domain=email.split('@')[1],
                exc_info=True
            )
            raise
    
    def create_user(self,*,email,password) -> User:
        try:
            user = User.objects.create_user(email=email, password=password)
            
            logger.info(
                "user_created",
                user_id=user.id,
                email_domain=email.split('@')[1],
            )
            
            return user
            
        except Exception as e:
            logger.error(
                "user_creation_failed",
                error=str(e),
                email_domain=email.split('@')[1],
                exc_info=True
            )
            raise
