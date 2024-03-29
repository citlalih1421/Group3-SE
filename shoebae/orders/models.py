from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.utils import timezone

User = get_user_model()

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    shoe = models.ForeignKey('store.Shoe', on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_ordered = models.DateTimeField(default=timezone.now)
 
class ShippingInfo(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_methods')
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(99999)])
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_default = models.BooleanField(default=False)
