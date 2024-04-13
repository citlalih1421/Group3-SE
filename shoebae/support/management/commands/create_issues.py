from django.core.management.base import BaseCommand
from support.models import Issue

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        issues = ['Technical', 'Purchase', 'Other']
        for issue in issues:
            try:
                Issue.objects.create(name=issue)
                #add logos eventually
                self.stdout.write(self.style.SUCCESS(f'Successfully created issue: {issue}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating issue "{issue}": {str(e)}'))
        self.stdout.write(self.style.SUCCESS('Issue creation process completed'))