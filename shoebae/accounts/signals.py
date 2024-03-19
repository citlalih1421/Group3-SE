from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission

@receiver(post_save, sender=User)
def assign_superuser_to_groups(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        # Define the group names you want to assign superusers to
        group_names = ['Buyer', 'Seller']
        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)
            permissions = Permission.objects.filter(content_type__app_label='your_app_label')
            group.permissions.set(permissions)
#def assign_user_to_groups(sender, instance, created, **kwargs):
    
