from django.urls import path
from accounts.views import RegisterAPIView, VerifyOTPAPIView, LoginAPIView, RefreshTokenAPIView
urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("verify-otp/", VerifyOTPAPIView.as_view(), name="verify-otp"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", RefreshTokenAPIView.as_view(), name="refresh")
]