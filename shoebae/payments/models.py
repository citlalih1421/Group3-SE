from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class PaymentInfo(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_information')
    card_holder = models.CharField(blank=True, null=True)
    card_number = models.IntegerField(blank=True, null=True)
    card_expiration = models.DateField(blank=True, null=True)
    card_cvv = models.IntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_default = models.BooleanField(default=False)