from django.urls import path
from accounts.views import RegisterAPIView, VerifyOTPAPIView
urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name='register'),
    path("verify-otp/", VerifyOTPAPIView.as_view(), name='verify-otp'),
]