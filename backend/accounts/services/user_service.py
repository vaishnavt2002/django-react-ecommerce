from accounts.repositiories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def create_user_from_verified_data(self, *, email: str, raw_password: str):
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("User already exists")
        
        return self.user_repo.create_user(email=email, password=raw_password)