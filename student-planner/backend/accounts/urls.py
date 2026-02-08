from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LoginStep1View, LoginStep2View

urlpatterns = [
    # Registeration
    path('register/', RegisterView.as_view(), name='register'),

    # Two-step login
    path('login-step1/', LoginStep1View.as_view(),name='login-step1'),
    path('login-step2/', LoginStep2View.as_view(), name='login-step2'),
    
    # token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]