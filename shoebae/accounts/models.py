from django.db import models
from django.contrib.auth.models import Group as BaseGroup

# Create your models here.

class UserType(BaseGroup):
    description = models.TextField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'User Type'
        verbose_name_plural = 'User Types'

    def __str__(self):
        return self.name
    
class Buyer(models.Model):
    
    class Meta:
        permissions = [('can_view_buyer', 'Can view buyer'),
                       ('can_edit_buyer', 'Can edit buyer')]

class Seller(models.Model):
    
    class Meta:
        permissions = [('can_view_seller', 'Can view seller'),
                       ('can_edit_seller', 'Can edit seller')]

