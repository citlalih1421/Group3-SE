from django.core.management.base import BaseCommand
from store.models import Brand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        brands = ['Nike','Adidas','Converse','Birkenstock','Valentino','Durango']
        for brand in brands:
            try:
                Brand.objects.create(name=brand)
                #add logos eventually
                self.stdout.write(self.style.SUCCESS(f'Successfully created brand: {brand}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating brand "{brand}": {str(e)}'))
        self.stdout.write(self.style.SUCCESS('Brand creation process completed'))