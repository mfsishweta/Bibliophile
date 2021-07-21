from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, VerifyOTPView, ResendOTPView, LoginView, SignupView

urlpatterns = [
    path('login', LoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path("verify-otp", VerifyOTPView.as_view(), name="verify otp"),
    path("resend-otp", ResendOTPView, name="resend otp"),
]
