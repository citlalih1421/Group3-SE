from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

#OVERALL TO-DO: implement __str__ methods (just ask chatgpt what they should be lol)
'''TO-DO: 
    Seller Model
    Ticekt Model
    Review Model
    Admin Model (implementing built-in superuser model, save this for last)
    '''

class PaymentInfo(models.Model): #INCOMPLETE: missing fields and methods
    user = models.OneToOneField(AbstractUser, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=255)
    credit_card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)
    #TO-DO: install django-encrypted-fields and change these to encrypted fields after import
    #end of PaymentInfo Model

class ShippingInfo(models.Model): #INCOMPLETE: missing methods
    user = models.OneToOneField(AbstractUser,on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    #end of ShippingInfo Model

class ShoeCategory(models.Model): #INCOMPLETE: missing fields and methods
    name = models.CharField(max_length=100)
    #TO-DO: find more things to be associated with a given category
    '''To-DO: hardcode predefined shoe category objects in different file
    stay away from this to-do john, it will get weird(running, lifting, etc)'''
    #end of ShoeCategory Model

class Shoe(models.Model): #INCOMPLETE: missing fields and methods
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    categories = models.ManyToManyField(ShoeCategory, symmetrical=False) #TO-DO
    shoe_picture = models.ImageField(upload_to='location/') #TO-DO get directory for image of shoe
    #end of Shoe Model

class ShoppingCart(models.Model): #INCOMPLETE: missing fields and methods
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE)
    shoes = models.ManyToManyField(Shoe, through='CartShoe')
    #end of ShoppingCart Model

class Inventory(models.Model): #INCOMPLETE: missing fields and methods
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    #end of Inventory Model

class Order(models.Model): #INCOMPLETE: missing fields and methods
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    shoes = models.ManyToManyField(Shoe, through='OrderID')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.buyer.user.username} on {self.order_date}"
    #end of Order Model


class Buyer(models.Model): #INCOMPLETE: missing methods
    user = models.OneToOneField(AbstractUser, on_delete=models.CASCASE)
    payment_info = models.OneToOneField(PaymentInfo, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_info = models.OneToOneField(ShippingInfo, on_delete=models.SET_NULL, null=True, blank=True)
    shopping_cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    reviews = models.ManyToManyField(Review)
    #end of Buyer Model
