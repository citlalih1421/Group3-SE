from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from store.models import Shoe
from django.utils import timezone

User = get_user_model()

# Create your models here
 
class ShippingInfo(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_methods')
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(99999)])
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    
class OrderItem(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.SET_NULL, null=True, related_name='order_items')
    quantity = models.IntegerField(default=0, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return str(self.id)
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    items = models.ManyToManyField(OrderItem)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shippinginfo = models.ForeignKey(ShippingInfo, on_delete=models.CASCADE, null=True)
    is_refunded = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.id)

