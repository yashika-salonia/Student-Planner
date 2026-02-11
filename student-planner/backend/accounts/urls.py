from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginStep1View, LoginStep2View, VerifyEmailView, ResendVerificationView

urlpatterns = [
    # Registeration
    path('register/', RegisterView.as_view(), name='register'),

    # verification of email
    path('verify-email/<uuid:token>/',VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),

    # Two-step login
    path('login-step1/', LoginStep1View.as_view(),name='login-step1'),
    path('login-step2/', LoginStep2View.as_view(), name='login-step2'),
    
    # token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]