from accounts.models import User

class UserRepository:
    def get_by_email(self, email: str):
        return User.objects.filter(email=email).first()
    
    def create_user(self,*,email,password):
        return User.objects.create_user(email=email, password=password)
