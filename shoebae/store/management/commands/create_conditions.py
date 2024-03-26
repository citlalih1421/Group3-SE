from django.core.management.base import BaseCommand
from store.models import Condition

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        conditions = ['New','Like New','Good','Fair','Poor']
        for condition in conditions:
            try:
                Condition.objects.create(name=condition)
                self.stdout.write(self.style.SUCCESS(f'Successfully created condition: {condition}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating condition "{condition}": {str(e)}'))
        self.stdout.write(self.style.SUCCESS('Condition creation process completed'))