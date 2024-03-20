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

def addLisiting(request):
    context = {}
    return render(request, 'store/addlisting.html')

def productPage(request):
    context = {}
    return render(request, 'store/productpage.html')

def seller(request):
    context = {}
    return render(request, 'store/seller.html')