from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class PaymentInfo(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_information')
    card_holder = models.CharField(blank=True, null=True)
    card_number = models.BinaryField(blank=True, null=True)
    card_expiration = models.BinaryField(blank=True, null=True)
    card_cvv = models.BinaryField(blank=True, null=True)
    is_default = models.BooleanField(default=False)