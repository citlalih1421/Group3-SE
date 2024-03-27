from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import ListView
from .forms import ShoeForm
from .models import Shoe, Condition, Brand, Category
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

# Create your views here.
def store(request):
    context = {}
    return render(request, 'store/store.html')

def cart(request):
    context = {}
    return render(request, 'store/cart.html')

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html')

def home(request):
    context = {}
    return render(request, 'store/home.html')

def add_listing(request): #remove this
    context = {}
    return render(request, 'store/addlisting.html')

def productpage(request):
    context = {}
    return render(request, 'store/productpage.html')

def seller(request):
    context = {}
    return render(request, 'store/seller.html')



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
    


    
class ShoeSearchListView(ListView):
    model = Shoe
    template_name = 'search.html'
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



class DeleteListingView(DeleteView):
    model = Shoe
    success_url = reverse_lazy('view_listings')
    template_name = 'store/delete_listing.html'  # Create this template if you want to customize the delete confirmation page