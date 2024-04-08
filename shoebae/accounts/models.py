from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

# Define UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

class PaymentInfo(models.Model):
    cardholder = models.CharField(max_length=100)
    cardnumber = models.CharField(max_length=19)
    expiration = models.DateField()
    cvv = models.CharField(max_length=4)
    balance = models.IntegerField()
    is_default = models.BooleanField(default=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cardholder}'s Payment Info"

class ShippingInfo(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} - Shipping Info"