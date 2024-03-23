from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:  # Check if a new user is created
        user_profile, _ = UserProfile.objects.get_or_create(user=instance)
        # Check conditions and assign user to appropriate group(s)
        if user_profile.is_buyer:
            buyer_group = Group.objects.get(name='Buyer')
            instance.groups.add(buyer_group)
        if user_profile.is_seller:
            seller_group = Group.objects.get(name='Seller')
            instance.groups.add(seller_group)
