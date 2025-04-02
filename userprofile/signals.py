# userprofile/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from accounting.models import CustomUser
from .models import UserProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, first_name=instance.first_name)

