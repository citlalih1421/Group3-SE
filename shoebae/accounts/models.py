from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_buyer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
