from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render, redirect


# Create your views here.

def register(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password2')
        password2 = request.POST.get('password2')
        is_buyer = request.POST.get('is_buyer')
        is_seller = request.POST.get('is_seller')

        #verfies valid and unused email
        if (not '@' in email) or (User.objects.filter(email=email).exists()):
            messages.error(request, 'Invalid email address')
            return render(request, 'accounts/register.html')
        
        #verifies unique username
        if (User.objects.filter(username=username)):
            messages.error(request, 'Username is already taken')
            return render(request, 'accounts/register.html')
        
        #verifies password was confirmed
        if (password1 != password2):
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html')
        
        #creates the user and stores their registration information
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password1, 
            first_name=first_name, 
            last_name=last_name
            )
        group_buyer, created = Group.objects.get_or_create(name='Buyer')
        group_seller, created = Group.objects.get_or_create(name='Seller')
        if (is_buyer):
            user.groups.add(group_buyer)

        if (is_seller):
            user.groups.add(group_seller)

        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('login')
        
    return render(request, 'accounts/register.html')

def login_view(request):
    if (request.method == 'POST'):
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        user=None
        if ('@' in username_or_email):
            user = authenticate(email=username_or_email,password=password)
        else:
            user = authenticate(username=username_or_email,password=password)

        if (user is not None):
            login(request,user=user)
            return redirect('store')
        else:
            messages.error(request, 'Invalid username or email')
            return render(request,'accounts/login.html')
        
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('store')

def account_view(request):
    user_groups = Group.objects.filter(user=request.user)
    context = {
        'user' : request.user,
        'user_groups': user_groups
    }
    return render(request, 'accounts/my_account/account.html', context)

def account_information_view(request):
    context = {}
    return render(request, 'accounts/my_account/account_information.html')

def security_view(request):
    context = {}
    return render(request, 'accounts/my_account/security.html')

def payment_methods_view(request):
    context = {}
    return render(request, 'accounts/my_account/payment_methods.html')

def shipping_methods_view(request):
    context = {}
    return render(request, 'accounts/my_account/shipping_methods.html')

def order_history_view(request):
    context = {}
    return render(request, 'accounts/my_account/order_history.html')

def tickets_view(request):
    context = {}
    return render(request, 'accounts/my_account/tickets.html')