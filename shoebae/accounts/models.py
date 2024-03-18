from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#To-Do, implement the encryption methods with the database in views. Encrypted information is stored in binary.
#To-DO, Favorites, Ticket, Tickets models

# Create your models here.

class PaymentInfo(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_infos')
    card_holder = models.CharField(blank=True, null=True) #does not need to be encrypted
    card_number = models.BinaryField(blank=True, null=True) #not sure how to show just last 4/5 numbers of card
    card_expiration = models.BinaryField(blank=True, null=True) #not sure how MM/YYYY is going to be encrypted exactly
    card_cvv = models.BinaryField(blank=True, null=True)
    is_default = models.BooleanField(default=False)

class ShippingInfo(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_infos')
    street = models.BinaryField(blank=True, null=True)
    city = models.BinaryField(blank=True, null=True)
    zipcode = models.BinaryField(blank=True, null=True)
    state = models.BinaryField(blank=True, null=True)
    country = models.BinaryField(blank=True, null=True)
    is_default = models.BooleanField(default=False)