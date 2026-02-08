import random
import string
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import socket

def generate_otp():
    """Generate a 6-digit numeric OTP."""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(user_email, otp_code):
    """Send OTP via email"""

    subject='Your login verification code - Student Planner'

    message=f"""
Hello!

Your Verification code is: {otp_code}

This code wil expire in 5 minutes.

If u didn't request this code, please ignore this email.

Stay peoductive! 
- Student Planner Team

Need help? Reply to this email.
    """
    
    try:
        result=send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False,
        )
        if result==1:
            print(f"Email sent successfully to {user_email}")
            return True
        else:
            print(f"Email send failed (result: {result})")
            return False
        
    except socket.gaierror as e:
        print(f"Network error- cannot reach email server: {e}")
        return False
    
    except Exception as e:
        print(f"Error sending email to {user_email}: {str(e)}")
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
    
    expiry_time = user_profile.otp_created_at + timedelta(minutes=5)

    current_time=timezone.now()
    
    return current_time < expiry_time