from accounts.repositiories.user_repository import UserRepository
from django.contrib.auth import get_user_model
User = get_user_model()

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def user_exist(self, *, email: str):
        return User.objects.filter(email=email).exists()


    def create_user_from_verified_data(self, *, email: str, raw_password: str):
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("User already exists")
        
        return self.user_repo.create_user(email=email, password=raw_password)