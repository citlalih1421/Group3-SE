from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.utils import timezone


User = get_user_model()

# Create your models here.
def increment_by_half_validator(value):
    if value % 0.5 != 0:
        raise ValidationError('Value must be incrementable by 0.5.')

def upload_image_path(instance, filename):
    # Generate upload path based on seller's ID and product's ID
    seller_id = instance.seller.id
    return f'sellers/{seller_id}/{filename}'

class Condition(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='images/brands/', blank=True, null=True)

    def __str__(self):
        return self.name

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name', 'parent']

    def __str__(self):
        return self.name
    
class Shoe(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_image_path)
    quantity = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(5000),
            DecimalValidator(max_digits=10, decimal_places=2)
        ]
    )
    size = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(1),
            DecimalValidator(max_digits=3, decimal_places=1)
        ]
    )
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True, default='')
    is_approved = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's not already set
            self.slug = slugify(self.name)  # Generate slug from the shoe's name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.SET_NULL, null=True, related_name='cart_item')
    item_quantity = models.IntegerField(default=0, null=True, blank=True)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.shoe.name

class ShoppingCart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.PROTECT, related_name='shopping_cart')
    cart_items = models.ManyToManyField(CartItem)
    cart_quantity = models.IntegerField(default=0, null=True, blank=True)
    cart_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def reset_cart(self):
        # Delete all cart items associated with this shopping cart
        for item in self.cart_items.all():
            item.delete()

        # Reset other values to zero
        self.cart_quantity = 0
        self.cart_total = 0

        # Save the changes to the shopping cart
        self.save()

    def __str__(self):
        return f"{self.customer.get_username()}'s cart"
    
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', null=True)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
            DecimalValidator(max_digits=2, decimal_places=1),
            increment_by_half_validator
        ]
    )
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    


class Favorite(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)

