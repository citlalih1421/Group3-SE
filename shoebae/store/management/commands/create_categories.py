from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        categories = {
            'Mens': ['Sneakers','Boots','Slippers','Casual','Sandals & Flip Flops'],
            'Womens': ['Sneakers', 'Boots', 'Slippers', 'Sandals & Flip Flops', 'Flats & Loafers', 'Clogs & Mules', 'Heels & Wedges'],
            'Kids': {'Boys': ['Sneakers','Boots','Slides','Casual','Sandals & Flip Flops'], 'Girls': ['Sneakers','Boots','Slides','Casual','Sandals & Flip Flops']}
        }

        for primary, secondary in categories.items():
            primary_category = Category.objects.create(name=primary)

            if isinstance(secondary, list):  # For Mens and Womens
                for sub_category_name in secondary:
                    try:
                        Category.objects.create(name=sub_category_name, parent=primary_category)
                        self.stdout.write(self.style.SUCCESS(f'Successfully created category: {sub_category_name} under {primary}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error creating category "{sub_category_name}": {str(e)}'))
            else:  # For Kids
                for sub_primary, sub_secondary in secondary.items():
                    sub_primary_category = Category.objects.create(name=sub_primary, parent=primary_category)

                    for sub_category_name in sub_secondary:
                        try:
                            Category.objects.create(name=sub_category_name, parent=sub_primary_category)
                            self.stdout.write(self.style.SUCCESS(f'Successfully created category: {sub_category_name} under {sub_primary}'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Error creating category "{sub_category_name}": {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Category creation process completed'))