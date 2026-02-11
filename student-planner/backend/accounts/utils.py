import random
import string
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
# import socket

def generate_otp():
    """Generate a 6-digit numeric OTP."""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(user_email, username, verification_token):
    """
    send verification link
    Args:
        user_email= user's email
        username:''
        verificaton_token=UUID token for verification

    Returns:
        True if sent successfully, False otherwise

    """

    verification_link = f"http://localhost:8000/api/auth/verify-email/{verification_token}/"

    expiry_hours=getattr(settings, 'EMAIL_VERIFICATION_EXPIRY_HOURS', 24)

    subject='Verify Your email - Student Planner'
    message=f"""
Hello {username}!

Welcome to Student Planner!

Please verify your email address by clicking the link below:
{verification_link}

This will expire in {expiry_hours} hours.

If u didn't created this account, you can safely ignore this email.

Stay productive!
-Student Planner Team
"""
    try:
        result = send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False,
        )

        if result == 1:
            print(f"Verification email sent to {user_email}")
            print(f"Verifiaction link: {verification_link}")
            return True
        else:
            # print(f"Verification email failed")
            return False
    except Exception as e:
        print(f"Error sending verification email: {str(e)}")
        return False

def send_otp_email(user_email, otp_code):
    """Send OTP via email"""

    expiry_minutes=getattr(settings, 'OTP_EXPIRY_MINUTES', 5)

    subject='Your login verification code - Student Planner'

    message=f"""
Hello!

Your Verification code is: {otp_code}

This code wil expire in {expiry_minutes}  minutes.

If u didn't request this code, please ignore this email.

Stay peoductive! 
- Student Planner Team
"""
    
    try:
        result=send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False,
        )
        if result==1:
            print(f"OTP sent to {user_email}")
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error:{str(e)}")
        return False

def is_otp_valid(user_profile):
    """Check if OTP is still valide
    Args: 
        user_profile: UserProfile object

    Returns:
        true if valid, false if expired or not sent
    """
    if not user_profile.otp_created_at:
        return False
    
    expiry_minutes=getattr(settings, 'OTP_EXPIRY_MINUTES', 5)
    
    expiry_time = user_profile.otp_created_at + timedelta(minutes=expiry_minutes)

    current_time=timezone.now()
    
    return current_time < expiry_time