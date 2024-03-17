from django.db import models
from django.contrib.auth.models import AbstractUser
from store.models import Shoe
from django.utils import timezone

#To-Do, implement the encryption methods with the database in views. Encrypted information is stored in binary.
#To-DO, Favorites, Ticket, Tickets models

# Create your models here.
class PaymentInfo(models.Model):
    card_holder = models.CharField(blank=True, null=True) #does not need to be encrypted
    card_number = models.BinaryField(blank=True, null=True) #not sure how to show just last 4/5 numbers of card
    card_expiration = models.BinaryField(blank=True, null=True) #not sure how MM/YYYY is going to be encrypted exactly
    card_cvv = models.BinaryField(blank=True, null=True)

class PaymentMethods(models.Model):
    payment_info = models.ManyToManyField(PaymentInfo)
    is_default_payment = models.BooleanField(default=False)

class ShippingInfo(models.Model):
    street = models.BinaryField(blank=True, null=True)
    city = models.BinaryField(blank=True, null=True)
    zipcode = models.BinaryField(blank=True, null=True)
    state = models.BinaryField(blank=True, null=True)
    country = models.BinaryField(blank=True, null=True)

class ShippingMethods(models.Model):
    shipping_info = models.ManyToManyField(ShippingInfo)
    is_default_shipping = models.BooleanField(default=False)

#class Ticket(models.Model):

#class Tickets(models.Model):
class Customer(AbstractUser):
    is_buyer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=True)
    payment_methods = models.OneToOneField(PaymentMethods, on_delete=models.CASCADE)
    shipping_methods = models.OneToOneField(ShippingMethods, on_delete=models.CASCADE)
    order_history = models.ManyToManyField('Order')
    favorites = models.ManyToManyField(Shoe)
    #tickets = models.OneToOneField(Tickets, on_delete=models.CASCADE)
    class Meta:
        app_label = "accounts"
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this customer belongs to. A customer will get all permissions granted to each of their groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this customer'
    )

class Order(models.Model): #add transaction id
    order_customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_shoe = models.ForeignKey(Shoe, on_delete=models.PROTECT)
    order_quantity = models.IntegerField(default=1,null=True,blank=True)
    date_ordered = models.DateTimeField(default=timezone.now)

class Buyer(models.Model):

    class Meta:
        permissions = [('can_view_buyer', 'Can view buyer'),
                       ('can_edit_buyer', 'Can edit buyer')]

class Seller(models.Model):
    
    class Meta:
        permissions = [('can_view_seller', 'Can view seller'),
                       ('can_edit_seller', 'Can edit seller')]

