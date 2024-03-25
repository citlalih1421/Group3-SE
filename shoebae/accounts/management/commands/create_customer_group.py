from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from payments.models import PaymentInfo
from orders.models import ShippingInfo
from support.models import Ticket
from store.models import Shoe

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Create Customer group
        customer_group, _ = Group.objects.get_or_create(name='Customer')
        
        model_permissions = {
            PaymentInfo: ('view_paymentinfo', 'add_paymentinfo','change_paymentinfo', 'delete_paymentinfo'),
            ShippingInfo: ('view_shippinginfo', 'add_shippinginfo','change_shippinginfo', 'delete_shippinginfo'),
            Ticket: ('view_ticket', 'add_ticket', 'change_ticket', 'delete_ticket'),
            Shoe: ['view_shoe']
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
                    customer_group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f"Added permission: {content_type.app_label}.{perm}"))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Permission does not exist: {content_type.app_label}.{perm}"))
