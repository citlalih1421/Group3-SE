from django.http import Http404, HttpResponseRedirect
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import ListView
from .forms import ShoeForm
from .models import Shoe, Condition, Brand, Category, ShoppingCart, CartItem
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from orders.models import Order
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_to_cart(request, slug):
    shoe = get_object_or_404(Shoe, slug=slug)
    shopping_cart, created = ShoppingCart.objects.get_or_create(customer=request.user)

    # Check if the item is already in the cart
    cart_item = shopping_cart.cartitem_set.filter(shoe=shoe).first()
    if cart_item:
        # If item exists, update its quantity using the update_quantity method from Shoe model
        shoe.update_quantity(quantity=cart_item.quantity + 1)
    else:
        # If item does not exist, create a new cart item
        cart_item = shopping_cart.cartitem_set.create(shoe=shoe, quantity=1)

    # Update shopping cart total using the method defined in the model
    shopping_cart.update_total()

    # Redirect to cart view with the shopping cart ID as a URL parameter
    return redirect('cart', cart_id=shopping_cart.id)

@login_required
def cart(request, cart_id):
    # Retrieve the shopping cart using the cart_id from the URL
    shopping_cart = get_object_or_404(ShoppingCart, id=cart_id)
    cart_items = shopping_cart.cartitem_set.all()

    # Calculate total for the cart
    total_amount = sum(item.shoe.price * item.quantity for item in cart_items)

    context = {'shopping_cart': shopping_cart, 'cart_items': cart_items, 'total_amount': total_amount}
    return render(request, 'store/cart.html', context)



def checkout(request):
    context = {}
    return render(request, 'store/checkout.html')

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
    
class ShoeSearchListView(ListView):
    model = Shoe
    template_name = 'filter.html'
    context_object_name = 'shoes'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        seller_username = self.request.GET.get('seller')
        queryset = super().get_queryset()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(brand__icontains=query) |
                Q(conditions__icontains=query) |
                Q(category__icontains=query)
            )
        if seller_username:
            queryset = queryset.filter(seller__username=seller_username)

        return queryset


class DeleteListingView(View):
    def post(self, request, slug):
        # Retrieve the listing based on the slug
        listing = get_object_or_404(Shoe, slug=slug)

        # Check if the confirmation parameter is present in the request
        if request.POST.get('confirmation') == 'true':
            # Perform deletion logic
            listing.delete()
            return redirect('store')  # Redirect to the desired URL after deletion
        else:
            # Handle case where confirmation is not provided
            error_message = "Confirmation was not provided. Deletion was not performed."
            return render(request, 'store/store.html', {'error_message': error_message})



