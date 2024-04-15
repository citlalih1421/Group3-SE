from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.utils import timezone


User = get_user_model()

# Create your models here.
def increment_by_half_validator(value):
    if value % 0.5 != 0:
        raise ValidationError('Value must be incrementable by 0.5.')

def upload_image_path(instance, filename):
    # Generate upload path based on seller's ID and product's ID
    seller_id = instance.seller.id
    return f'sellers/{seller_id}/{filename}'

class Condition(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='images/brands/', blank=True, null=True)

    def __str__(self):
        return self.name

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name', 'parent']

    def __str__(self):
        return self.name
    
class Shoe(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_image_path)
    quantity = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(5000),
            DecimalValidator(max_digits=10, decimal_places=2)
        ]
    )
    size = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(1),
            DecimalValidator(max_digits=3, decimal_places=1)
        ]
    )
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True, default='')
    is_approved = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's not already set
            self.slug = slugify(self.name)  # Generate slug from the shoe's name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', null=True)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
            DecimalValidator(max_digits=2, decimal_places=1),
            increment_by_half_validator
        ]
    )
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
class Checkout(View):
    model = Order
    fields = []  # Assuming no specific fields need to be defined for Order creation

    def get(self, request):
        shopping_cart = request.user.shopping_cart
        cart_items = shopping_cart.cartitem_set.all()
        payment_info = PaymentInfo.objects.filter(customer=request.user, is_default=True).first()
        shipping_info = ShippingInfo.objects.filter(customer=request.user, is_default=True).first()
        total_items = sum(item.quantity for item in cart_items)

        context = {
            'shopping_cart': shopping_cart,
            'cart_items' : cart_items,
            'paymentinfo': payment_info,
            'shippinginfo': shipping_info,
            'total_items': total_items,
            'total_price': shopping_cart.total
        }
        return render(request, 'store/checkout.html', context)

    def post(self, request):
        shopping_cart = request.user.shopping_cart
        cart_items = shopping_cart.cartitem_set.all()
        payment_info = PaymentInfo.objects.filter(customer=request.user, is_default=True).first()
        shipping_info = ShippingInfo.objects.filter(customer=request.user, is_default=True).first()

        order_total = shopping_cart.total  # Store the total before setting it to 0
        order = Order.objects.create(
            customer=request.user,
            total=order_total,
            shippinginfo=shipping_info,
            date_ordered=timezone.now()
        )

        for item in cart_items:
            order_item = OrderItem.objects.create(
                shoe=item.shoe,
                quantity=item.quantity,
                total=item.subtotal  # Assuming subtotal is calculated correctly in CartItem model
            )
            order.items.add(order_item)  # Add the order item to the order
            # Optionally delete the cart item
            item.delete()

            # Distribute payment to seller
            seller_payment_info = item.shoe.seller.payment_info  # Assuming Shoe has a OneToOneField to Seller with a payment_info field
            seller_payment_info.balance += item.subtotal
            seller_payment_info.save()

        shopping_cart.total = 0
        shopping_cart.save()  # Save the updated total to the database

        payment_info.balance -= order_total  # Deduct the order total from the balance
        payment_info.save()

        return redirect('order', order=order.id)

class Favorite(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)

