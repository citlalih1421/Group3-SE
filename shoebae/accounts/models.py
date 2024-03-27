from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Define UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
