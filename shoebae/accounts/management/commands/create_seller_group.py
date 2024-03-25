from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from store.models import Shoe

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Create Seller group
        seller_group, _ = Group.objects.get_or_create(name='Seller')

        model_permissions = {
            Shoe: ('add_shoe','change_shoe', 'delete_shoe')
        }

        # Loop to apply the permissions
        for model, permissions in model_permissions.items():
            content_type = ContentType.objects.get_for_model(model)
            for perm in permissions:
                try:
                    permission = Permission.objects.get(
                        content_type=content_type,
                        codename=perm
                    )
                    seller_group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f"Added permission: {content_type.app_label}.{perm}"))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Permission does not exist: {content_type.app_label}.{perm}"))
