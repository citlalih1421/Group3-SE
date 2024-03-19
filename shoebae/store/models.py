from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from decimal import Decimal 

# Create your models here.
def increment_by_half_validator(value):
    if value % 0.5 != 0:
        raise ValidationError('Value must be incrementable by 0.5.')

class Shoe(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/shoes/')
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
    conditions = models.CharField(
        max_length=100,
        default='other'
    )
    brand = models.CharField(
        max_length=100,
        default='other'
    )
    category = models.CharField(
        max_length=255,
        default='other'
    )
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

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
    parent = TreeForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
    class MPTTMeta:
        order_insertion_by = ['name','parent']

    def __str__(self):
        return self.name
    
class Review(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    rating = models.DecimalField(
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
        return self.title
    
class Order(models.Model): #add transaction id
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    shoe = models.ForeignKey(Shoe, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1,null=True,blank=True)
    date_ordered = models.DateTimeField(default=timezone.now)

class Favorite(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)

#represents a shopping cart belonging to the user
class ShoppingCart(models.Model):                                                   
    customer = models.OneToOneField(User, on_delete = models.CASCADE)  #OneToOne relationship because each user has one cart
    items = models.ManyToManyField('Shoe', through='cartitem')         #ManyToMany relationship this allows a single shoe to be associated with many carts

#represents an item in the shopping cart
class CartItem(models.Model):
    shoe = models.ForeignKey('Shoe', on_delete=models.CASCADE)        #defines a foreign key named shoe and says if the shoe is deleted so will the cart item be
    shopping_cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE)  #defines a foreign key named shopping cart and will delete the items if the shopping cart is deleted
    quantity = models.IntegerField(default=1)                          #represents a quantity associated with the shopping cart and if the quntity is not given it will be 1
    date_added = models.DateTimeField(default=timezone.now)            #represents the date the shopping cart was made and it will pull from the timezone.now
    