from decimal import Decimal
from django.db import IntegrityError
<<<<<<< Updated upstream
from django.http import HttpResponse  # Import HttpResponse for debugging
from django.http import Http404, HttpResponseRedirect
=======
>>>>>>> Stashed changes
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import ListView
from .forms import ShoeForm
from .models import Shoe, Condition, Brand, Category, ShoppingCart, CartItem
from django.urls import reverse_lazy
from orders.models import Order, OrderItem, ShippingInfo
from payments.models import PaymentInfo
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from django.utils import timezone
from django.contrib import messages
<<<<<<< Updated upstream
from django.urls import reverse
=======
>>>>>>> Stashed changes


# Create your views here.
@login_required
def add_to_cart(request, slug):
    shoe = get_object_or_404(Shoe, slug=slug)
    shopping_cart, created = ShoppingCart.objects.get_or_create(customer=request.user)

    # Check if the shoe is already in the cart
    cart_item, created = CartItem.objects.get_or_create(shoe=shoe, defaults={'item_quantity': 1, 'item_total': shoe.price})
    if not created:
        cart_item.item_quantity += 1
        cart_item.item_total += shoe.price
        cart_item.save()
        shopping_cart.cart_total += shoe.price
        shopping_cart.save()

    # Add the cart item to the shopping cart if not already there
    if cart_item not in shopping_cart.cart_items.all():
        shopping_cart.cart_items.add(cart_item)
        shopping_cart.cart_quantity += 1  # Increment cart quantity
        shopping_cart.cart_total += cart_item.shoe.price
        shopping_cart.save()

    # Redirect to cart view with the shopping cart ID as a URL parameter
    return redirect('cart', cart_id=shopping_cart.id)

@login_required
def cart(request, cart_id):
    # Retrieve the shopping cart using the cart_id from the URL
    shopping_cart = get_object_or_404(ShoppingCart, id=cart_id)
    cart_items = shopping_cart.cart_items.all()

    context = {'shopping_cart': shopping_cart, 'cart_items': cart_items}
    return render(request, 'store/cart.html', context)

class Checkout(View):
    model = Order
    fields = []  # Assuming no specific fields need to be defined for Order creation

    def get(self, request):
        shopping_cart = request.user.shopping_cart
        cart_items = shopping_cart.cart_items.all()
        payment_info = PaymentInfo.objects.filter(customer=request.user, is_default=True).first()
        shipping_info = ShippingInfo.objects.filter(customer=request.user, is_default=True).first()
        context = {
            'shopping_cart': shopping_cart,
            'cart_items' : cart_items,
            'paymentinfo': payment_info,
            'shippinginfo': shipping_info,
            'total_items': shopping_cart.cart_quantity
        }
        return render(request, 'store/checkout.html', context)
    
    def post(self, request):
        action = request.POST.get('action')

        if action == 'process_order':
            shopping_cart = request.user.shopping_cart
            shipping_info = ShippingInfo.objects.filter(customer=request.user, is_default=True).first()
            order_total = shopping_cart.cart_total
            try:
                order = Order.objects.create(
                    customer=request.user,
                    total=order_total,
                    shippinginfo=shipping_info
                )
                order.save()
                self.process_order_items(request, order)
                self.process_payments(request, order)
                messages.success(request, 'Order has been successfully processed!')
                return redirect('order', order_id=order.id)
            except IntegrityError:
                messages.error(request, 'Error processing order.')
        return redirect('checkout')

    def process_order_items(self, request, order):
        if order:
            shopping_cart = request.user.shopping_cart
            cart_items = shopping_cart.cart_items.all()
        
            for item in cart_items:
                try:
                    order_item = OrderItem.objects.create(
                        shoe = item.shoe,
                        quantity = item.item_quantity,
                        total = item.item_total
                    )
                    order.items.add(order_item)
                except IntegrityError as e:
                    raise IntegrityError
            order.save()
            shopping_cart.reset_cart()

        self.process_payments(request, order)

    def process_payments(self, request, order):
        if order:
            buyer = request.user.userprofile
            buyer.balance -= order.total
            buyer.save()
            order_items = order.items.all()
            for item in order_items:
                try:
                    seller = item.shoe.seller.userprofile
                    seller.balance += item.total
                    seller.save()
                except IntegrityError as e:
                    raise IntegrityError
            messages.success(request, 'Order has been successfully processed!')
            return redirect('order', order_id = order.id)

    '''def post(self, request):
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
            #pays each seller for the purchase
            order_seller = order_item.shoe.seller
            seller_payment = PaymentInfo.objects.filter(customer=order_seller, is_default=True).first()
            seller_payment.balance += order_item.total
            seller_payment.save()
            order.items.add(order_item)  # Add the order item to the order
            # Optionally delete the cart item
            item.delete()

        shopping_cart.total = 0
        shopping_cart.save()  # Save the updated total to the database

        payment_info.balance -= order_total  # Deduct the order total from the balance
        payment_info.save()

        return redirect('order', order_id=order.id)  # Redirect to the home page after checkout'''


def home(request):
    context = {}
    return render(request, 'store/home.html')

def add_listing(request): #remove this
    context = {}
    return render(request, 'store/addlisting.html')


class ProductPageView(DetailView):
    model = Shoe
    template_name = 'store/productpage.html'
    context_object_name = 'shoe'
    slug_url_kwarg = 'slug'  # Specify the slug URL keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(slug=self.kwargs[self.slug_url_kwarg])


def seller(request):
    context = {}
    return render(request, 'store/seller.html')

def filter(request):
    context = {}
    return render(request, 'store/filter.html')

def testing(request):
    context = {}
    return render(request, 'store/testing.html')

def paymentmethod(request):
    context = {}
    return render(request, 'store/paymentmethod.html')

def viewlisting(request):
    context = {}
    return render(request, 'store/viewlisting.html')



class AddListingView(CreateView):
    model = Shoe
    form_class = ShoeForm
    template_name = 'store/addlisting.html'
    success_url = 'listing'  # Replace this with your actual success URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        # Arrange categories in a hierarchical structure
        structured_categories = self.get_structured_categories(categories)
        context['categories'] = structured_categories
        context['brands'] = Brand.objects.all()
        context['conditions'] = Condition.objects.all()
        return context

    def get_structured_categories(self, categories):
        structured_categories = []
        for category in categories:
            if category.parent is None:
                # This is a top-level category
                structured_categories.append({
                    'category': category,
                    'children': self.get_children(category, categories),
                })
        return structured_categories

    def get_children(self, parent_category, all_categories):
        children = []
        for category in all_categories:
            if category.parent == parent_category:
                children.append({
                    'category': category,
                    'children': self.get_children(category, all_categories),
                })
        return children

    def form_valid(self, form):
        shoe = form.save(commit=False)
        shoe.seller = self.request.user
        shoe.save()
        return redirect(self.success_url)

def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')

            # Perform search based on form data
            shoes = Shoe.objects.all()  # Initial queryset

            if search_query:
                # Split the search query into keywords
                keywords = search_query.split()
                for keyword in keywords:
                    # Check if keyword matches any field in Shoe model
                    shoes = shoes.filter(
                        Q(name__icontains=keyword) |
                        Q(price__icontains=keyword) |
                        Q(brand__name__icontains=keyword) |
                        Q(condition__name__icontains=keyword) |
                        Q(category__name__icontains=keyword) |
                        Q(seller__username__icontains=keyword) |  # Search by seller's username
                        Q(is_approved__icontains=keyword)  # Filter by approved listings, must type True or False for now
                    ).distinct()

            return render(request, 'store/search_results.html', {'form': form, 'shoes': shoes})
    else:
        form = SearchForm()

    return render(request, 'store/search_results.html', {'form': form, 'shoes': None})

class ViewListingsView(ListView):
    model = Shoe
    template_name = 'store/mylistings.html'
    context_object_name = 'seller_listings'

    def get_queryset(self):
        # Filter listings to display only those associated with the currently logged-in user
        return Shoe.objects.filter(seller=self.request.user)
    

class ViewAllListingsView(ListView):
    model = Shoe
    template_name = 'store/store.html'
    context_object_name = 'listings'

    def get_queryset(self):
        queryset = Shoe.objects.all().order_by('-date_posted')
        return queryset


class DeleteListingView(View):
    def post(self, request, slug):
        # Retrieve the listing based on the slug
        listing = get_object_or_404(Shoe, slug=slug)
        if request.POST:
            # Perform deletion logic
            listing.delete()
            return redirect('store')  # Redirect to the desired URL after deletion



def compare_products(request):
    if request.method == 'POST':
        # Clear the comparison list from session
        request.session['comparison'] = []
        return redirect('compare_products')  # Redirect to the same page after clearing the comparison

    # Retrieve the slugs of shoes in the comparison list from session
    comparison_slugs = request.session.get('comparison', [])

    # Filter the Shoe objects based on slugs
    shoes_to_compare = Shoe.objects.filter(slug__in=comparison_slugs)

    context = {
        'shoes_to_compare': shoes_to_compare,
    }
    return render(request, 'store/compare.html', context)

def add_to_comparison(request, slug):
    # Retrieve the shoe object based on the slug
    shoe = get_object_or_404(Shoe, slug=slug)

    # Ensure the comparison list exists in the session
    if 'comparison' not in request.session:
        request.session['comparison'] = []

    # Check if the product is already in the comparison list
    if slug in request.session['comparison']:
        messages.warning(request, "Product is already in comparison.")
    else:
        # Check if the comparison list has reached its maximum limit
        if len(request.session['comparison']) >= 3:
            messages.error(request, "Maximum limit reached. You can compare up to three products.")
        else:
            # Add the product to the comparison list
            request.session['comparison'].append(slug)
            messages.success(request, "Product added to comparison.")

    # Redirect to the product page
    return redirect(reverse('productpage', args=[slug]))
