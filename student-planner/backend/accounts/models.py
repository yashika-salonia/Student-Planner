from django.contrib.auth.models import User
from django.db import models
import uuid  

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # OTP fields
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    two_factor_enabled = models.BooleanField(default=True)
    
    # Email verification fields
    email_verified = models.BooleanField(default=False)

    verification_token = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True,
        null=False
    )
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    class Meta:
        verbose_name='User Profile'
        verbose_name_plural='User Profiles'