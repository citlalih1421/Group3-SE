from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command('create_customer_group', *args, **kwargs)
        call_command('create_buyer_group', *args, **kwargs)
        call_command('create_seller_group', *args, **kwargs)