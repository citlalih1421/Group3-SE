from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command('create_categories', *args, **kwargs)
        call_command('create_brands', *args, **kwargs)
        call_command('create_conditions', *args, **kwargs)