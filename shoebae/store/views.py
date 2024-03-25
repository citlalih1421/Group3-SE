from django.shortcuts import render

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

def addlisiting(request):
    context = {}
    return render(request, 'store/addlisting.html')

def productpage(request):
    context = {}
    return render(request, 'store/productpage.html')

def seller(request):
    context = {}
    return render(request, 'store/seller.html')

def apply(request):
    context = {}
    return render(request, 'store/apply.html')

def testing(request):
    context = {}
    return render(request, 'store/testing.html')

def filter(request):
    context = {}
    return render(request, 'store/filter.html')

def listings(request):
    context = {}
    return render(request, 'store/listings.html')
