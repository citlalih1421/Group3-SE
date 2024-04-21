from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class PaymentInfo(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_information')
    cardholder = models.CharField(blank=True, null=True)
    cardnumber = models.CharField(blank=True, null=True)
    expiration = models.DateField(blank=True, null=True)
    cvv = models.IntegerField(blank=True, null=True)
    is_default = models.BooleanField(default=False)