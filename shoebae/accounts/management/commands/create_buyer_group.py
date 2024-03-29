from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from orders.models import Order
from store.models import ShoppingCart, CartItem

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Create Buyer group
        buyer_group, _ = Group.objects.get_or_create(name='Buyer')
        
        model_permissions = {
            ShoppingCart: ('view_shoppingcart', 'change_shoppingcart', 'delete_shoppingcart'),
            CartItem: ('view_cartitem', 'add_cartitem','change_cartitem', 'delete_cartitem'),
            Order: ('view_order', 'add_order','change_order', 'delete_order')
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
                    buyer_group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f"Added permission: {content_type.app_label}.{perm}"))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Permission does not exist: {content_type.app_label}.{perm}"))
