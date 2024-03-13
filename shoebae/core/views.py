from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from . models import Category, Shoe

# Create your views here.
def home(request):
    return render(request,'home.html')

def shoe_details(request):
    shoe = get_object_or_404(Shoe, id)

def search(request):
    return render(request,'search.html')

def cart(request):
    return render(request, 'cart.html')