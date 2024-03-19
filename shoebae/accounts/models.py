from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from store.models import Shoe
from django.utils import timezone

#To-Do, implement the encryption methods with the database in views. Encrypted information is stored in binary.
#To-DO, Favorites, Ticket, Tickets models

# Create your models here.

class PaymentInfo(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_information')
    card_holder = models.CharField(blank=True, null=True) #does not need to be encrypted
    card_number = models.BinaryField(blank=True, null=True) #not sure how to show just last 4/5 numbers of card
    card_expiration = models.BinaryField(blank=True, null=True) #not sure how MM/YYYY is going to be encrypted exactly
    card_cvv = models.BinaryField(blank=True, null=True)
    is_default = models.BooleanField(default=False)

class ShippingInfo(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_information')
    street = models.BinaryField(blank=True, null=True)
    city = models.BinaryField(blank=True, null=True)
    zipcode = models.BinaryField(blank=True, null=True)
    state = models.BinaryField(blank=True, null=True)
    country = models.BinaryField(blank=True, null=True)
    is_default = models.BooleanField(default=False)

class Issue(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name','parent']

    def __str__(self):
        return self.name
    
class Ticket(MPTTModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket')
    title = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='parent_ticket')
    issue = models.CharField(
        max_length = 100,
        default = 'other'
    )
    product_id = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    
    class MPTTMeta:
        order_insertion_by = ['title','parent']
        
    def __str__(self):
        return self.title
