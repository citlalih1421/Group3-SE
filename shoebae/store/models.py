from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Condition(models.Model):
    condition_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.condition_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    brand_logo = models.ImageField(upload_to='images/brands/', blank=True, null=True)

    def __str__(self):
        return self.brand_name

class Category(MPTTModel):
    category_name = models.CharField(max_length=255)
    parent = TreeForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
    class MPTTMeta:
        order_insertion_by = ['category_name','parent']

    def __str__(self):
        return self.category_name

class Shoe(models.Model):
    #possibly seller
    shoe_name = models.CharField(max_length=255)
    shoe_image = models.ImageField(upload_to='images/shoes/')
    shoe_quantity = models.IntegerField() #needs negative prevention
    shoe_price = models.DecimalField(max_digits=10,decimal_places=2) #needs negative prevention
    shoe_size = models.DecimalField(max_digits=3,decimal_places=1)# needs negative prevention and increment of 0.5
    condition_choices = [(condition.condition_name) for condition in Condition.objects.all()]
    shoe_conditions = models.CharField(#changes to increment drop down thing
        max_length=100,
        choices=condition_choices,
        blank=True, #remove blank and null later
        null=True
    )
    brand_choices = [(brand.brand_name) for brand in Brand.objects.all()]
    shoe_brand = models.CharField(#changes to increment drop down thing
        max_length=100,
        choices=brand_choices,
        blank=True, #remove blank and null later
        null=True
    )
    category_choices = [(category.parent, category.category_name) for category in Category.objects.all()]
    shoe_category = models.CharField(#changes to increment drop down thing
        max_length=255,
        choices=brand_choices,
        blank=True, #remove blank and null later
        null=True
    )
    #shoe_reviews = models.ManyToManyField(Reviews)
    def __str__(self):
        return self.shoe_name #tweak this to be more specific
    
