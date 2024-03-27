from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.validators import EmailValidator
from django.shortcuts import render, redirect
from django.views.generic import View
from store.models import Shoe
from .models import UserProfile  # Import the UserProfile model

User = get_user_model()

class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_buyer = request.POST.get('is_buyer') == 'on'
        is_seller = request.POST.get('is_seller') == 'on'

        validator = EmailValidator()
        try:
            validator(email)
        except:
            messages.error(request, 'Invalid email address')
            return render(request, 'accounts/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Invalid email address')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return render(request, 'accounts/register.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.is_buyer = is_buyer
        user_profile.is_seller = is_seller
        user_profile.save()
        

        group_buyer, created_buyer = Group.objects.get_or_create(name='Buyer')
        group_seller, created_seller = Group.objects.get_or_create(name='Seller')

        if is_buyer:
            user.groups.add(group_buyer)

        if is_seller:
            user.groups.add(group_seller)

        messages.success(request, 'Account created successfully')
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        user = None
        if '@' in username_or_email:
            user = authenticate(email=username_or_email, password=password)
        else:
            user = authenticate(username=username_or_email, password=password)

        if user is not None:
            login(request, user=user)
            return redirect('store')
        else:
            messages.error(request, 'Invalid username or email')
            return render(request, 'accounts/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('store')


class MyAccountView(View):
    def get(self, request):
        user_groups = Group.objects.filter(user=request.user)
        context = {'user': request.user, 'user_groups': user_groups}
        return render(request, 'accounts/my_account/account.html', context)


class MyInfoView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/account_information.html')


class MySecurityView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/security.html')


class MyPaymentView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/payment_methods.html')


class MyShippingView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/shipping_methods.html')


class MyOrdersView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/order_history.html')


class MyTicketsView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/tickets.html')


'''class MyListingsView(View):
    def get(self, request):
        seller_listings = Shoe.objects.filter(seller=request.user)
        return render(request, 'my_listings.html', {'seller_listings': seller_listings})'''
