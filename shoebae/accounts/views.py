from decimal import Decimal
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin #only logged-in users will see MyAcountView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.validators import EmailValidator
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from store.models import Shoe, ShoppingCart
from .models import UserProfile  # Import the UserProfile model
from .forms import ShippingForm, PaymentForm
from payments.models import PaymentInfo
from orders.models import Order, ShippingInfo
import datetime
from django.contrib.auth.decorators import login_required

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

        shopping_cart = ShoppingCart.objects.get_or_create(
            customer=user
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
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or email')
            return render(request, 'accounts/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class MyAccountView(View):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(customer=request.user)
        payment_info = PaymentInfo.objects.filter(customer=request.user)
        shipping_info = ShippingInfo.objects.filter(customer=request.user)
        context = {
            'user': user,
            'orders': orders,
            'payment_info': payment_info,
            'shipping_info': shipping_info
        }
        return render(request, 'accounts/my_account/account.html', context)
    
    def post(self, request):
        if 'action' in request.POST:
            action = request.POST['action']

        if action == 'show_edit_payment_form':
            return self.show_edit_payment_form(request)
        elif action == 'process_edit_payment_form':
            return self.process_edit_payment_form(request)
        elif action == 'delete_payment':
            return self.delete_payment(request)
        elif action == 'show_add_payment_form':
            return self.process_add_payment_form(request)
        elif action == 'process_add_payment_form':
            return self.process_add_payment_form(request)
        elif action == 'process_add_shipping_form':
            return self.process_add_shipping_form(request)
        elif action == 'show_add_shipping_form':
            return self.show_add_shipping_form(request)
        elif action == 'show_edit_shipping_form':
            return self.show_edit_shipping_form(request)
        elif action == 'process_edit_shipping_form':
            return self.process_edit_shipping_form(request)
        elif action == "delete_shipping":
            return self.delete_shipping(request)
        elif action == "update_balance":
            return self.update_balance(request)
        else:
            return render(request, 'accounts/my_account/account.html', {'message': 'Invalid form submission'})
    
    def show_edit_payment_form(self, request):
        payment_info_id = request.POST.get('edit_payment_id')
        if payment_info_id:
            payment = get_object_or_404(PaymentInfo, id=payment_info_id, customer=request.user)
            form = PaymentForm(instance=payment)  # Pre-populate form with existing data
            return render(request, 'accounts/my_account/account.html', {'edit_payment_form': form, 'payment': payment})
        else:
            return render(request, 'accounts/my_account/account.html', {'message': 'Invalid edit request'})

    def process_edit_payment_form(self, request):
        payment_info_id = request.POST.get('edit_payment_id')
        payment_info = get_object_or_404(PaymentInfo, id=payment_info_id, customer=request.user)
        form = PaymentForm(request.POST, instance=payment_info)

        if form.is_valid():
            form.save()
            messages.success(request, "Payment method updated successfully!")
            return redirect('account')
        else:
            messages.error(request, "Error in updating payment method. Please try again.")
            return render(request, 'accounts/my_account/account.html', {'edit_payment_form': form, 'payment': payment_info})
        
    def delete_payment(self, request):
        payment_info_id = request.POST.get('delete_payment_id')
        payment_info = get_object_or_404(PaymentInfo, id=payment_info_id, customer=request.user)
        payment_info.delete()
        messages.success(request, "Payment method deleted successfully!")
        return redirect('account')
    
    def show_add_payment_form(self, request):
        form = PaymentForm()  # Create a new form instance
        return render(request, 'accounts/my_account/account.html', {'add_payment_form': form})

    def process_add_payment_form(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            new_payment_info = form.save(commit=False)
            new_payment_info.customer = request.user
            new_payment_info.save()
            messages.success(request, "Payment method added successfully!")
            return redirect('account')
        else:
            messages.error(request, "Error in adding payment method. Please try again.")
            payment_info = PaymentInfo.objects.filter(customer=request.user)
        return render(request, 'accounts/my_account/account.html', {'add_payment_form': form, 'payment_info': payment_info})
    
    def show_edit_shipping_form(self, request):
        shipping_info_id = request.POST.get('edit_shipping_id')
        if shipping_info_id:
            shipping = get_object_or_404(ShippingInfo, id=shipping_info_id, customer=request.user)
            form = ShippingForm(instance=shipping)  # Pre-populate form with existing data
            return render(request, 'accounts/my_account/account.html', {'edit_shipping_form': form, 'shipping': shipping})
        else:
            return render(request, 'accounts/my_account/account.html', {'message': 'Invalid edit request'})

    def process_edit_shipping_form(self, request):
        shipping_info_id = request.POST.get('edit_shipping_id')
        shipping_info = get_object_or_404(ShippingInfo, id=shipping_info_id, customer=request.user)
        form = ShippingForm(request.POST, instance=shipping_info)

        if form.is_valid():
            form.save()
            messages.success(request, "Shipping method updated successfully!")
            return redirect('account')
        else:
            messages.error(request, "Error in updating shipping method. Please try again.")
            return render(request, 'accounts/my_account/account.html', {'edit_shipping_form': form, 'shipping': shipping_info})
        
    def update_balance(self, request):
        new_balance = request.POST.get('new_balance')
        # Validate the new_balance input (ensure it's a valid number, etc.)
        if new_balance:
            try:
                new_balance = Decimal(new_balance)  # Convert to float
                request.user.userprofile.balance += new_balance
                request.user.userprofile.save()
                messages.success(request, 'Balance updated successfully.')
            except ValueError:
                messages.error(request, 'Invalid balance input.')
        else:
            messages.error(request, 'New balance value is required.')

        return redirect('account')  

    def delete_shipping(self, request):
        shipping_info_id = request.POST.get('delete_shipping_id')
        shipping_info = get_object_or_404(ShippingInfo, id=shipping_info_id, customer=request.user)
        shipping_info.delete()
        messages.success(request, "Shipping method deleted successfully!")
        return redirect('account')

    def show_add_shipping_form(self, request):
        form = ShippingForm()  # Create a new form instance
        return render(request, 'accounts/my_account/account.html', {'add_shipping_form': form})

    def process_add_shipping_form(self, request):
        form = ShippingForm(request.POST)
        if form.is_valid():
            new_shipping_info = form.save(commit=False)
            new_shipping_info.customer = request.user
            new_shipping_info.save()
            messages.success(request, "Shipping method added successfully!")
            return redirect('account')
        else:
            messages.error(request, "Error in adding shipping method. Please try again.")
            shipping_info = ShippingInfo.objects.filter(customer=request.user)
        return render(request, 'accounts/my_account/account.html', {'add_shipping_form': form, 'shipping_info': shipping_info})
    

class MyInfoView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/account_information.html')


class MySecurityView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/security.html')


class MyTicketsView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/tickets.html')

class MyFavoritesView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/favorites.html')
    




class DeleteAccountView(View):
    def get(self, request):
        return render(request, 'accounts/delete_account.html')

    def post(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')



'''class MyListingsView(View):
    def get(self, request):
        seller_listings = Shoe.objects.filter(seller=request.user)
        return render(request, 'my_listings.html', {'seller_listings': seller_listings})'''
class MySecurityView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/security.html')

    def post(self, request):
        # Retrieve the current user and delete their account
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        user.delete()
        
        # Log out the user
        logout(request)
        
        # Redirect to the home page or any other desired page
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  # Assuming 'home' is the name of your home page URL