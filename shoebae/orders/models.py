from django.db import models
from django.contrib.auth import get_user_model
from datetime import timezone

User = get_user_model()

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    shoe = models.ForeignKey('store.Shoe', on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_ordered = models.DateTimeField(default=timezone.now)

class ShoppingCart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shopping_cart')
    items = models.ManyToManyField('Shoe', through='CartItem')

class CartItem(models.Model):
    shoe = models.ForeignKey('store.Shoe', on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
 
class ShippingInfo(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_methods')
    street = models.BinaryField(blank=True, null=True)
    city = models.BinaryField(blank=True, null=True)
    zipcode = models.BinaryField(blank=True, null=True)
    state = models.BinaryField(blank=True, null=True)
    country = models.BinaryField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
