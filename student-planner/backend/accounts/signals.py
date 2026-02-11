from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
import logging

logger=logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwags):
    """
    Signal to automatically create UserProfile when User is created
    """
    if created:
        if not hasattr(instance, 'profile'):
            try:
                UserProfile.objects.create(user=instance)
                logger.info(f"Profile created for {instance.username}")
            except Exception as e:
                logger.error(f"Error creating profile for {instance.username}: {e}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save UserProfile when user is saved
    """
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except Exception as e:
        logger.error(f"Error saving profile for {instance.username}: {e}")