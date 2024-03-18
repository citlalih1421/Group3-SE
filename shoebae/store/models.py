from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from django.db import models
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from decimal import Decimal 

# Create your models here.
def increment_by_half_validator(value):
    if value % 0.5 != 0:
        raise ValidationError('Value must be incrementable by 0.5.')

class Shoe(models.Model):
    shoe_name = models.CharField(max_length=255)
    shoe_image = models.ImageField(upload_to='images/shoes/')
    shoe_quantity = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    shoe_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(5000),
            DecimalValidator(max_digits=10, decimal_places=2)
        ]
    )
    shoe_size = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(1),
            DecimalValidator(max_digits=3, decimal_places=1)
        ]
    )
    shoe_conditions = models.CharField(
        max_length=100,
        default='other'
    )
    shoe_brand = models.CharField(
        max_length=100,
        default='other'
    )
    shoe_category = models.CharField(
        max_length=255,
        default='other'
    )
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.shoe_name

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
    
class Review(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=255)
    review_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators= [
            MinValueValidator(1),
            MaxValueValidator(5),
            DecimalValidator(max_digits=2,decimal_places=1),
            increment_by_half_validator
        ]
    )
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.review_title
