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
        user = request.user
        user_groups = Group.objects.filter(user=user)
        
        is_seller = user.groups.filter(name='Seller').exists()
        is_buyer = user.groups.filter(name='Buyer').exists()
        
        context = {
            'user': user,
            'user_groups': user_groups,
            'is_seller': is_seller,
            'is_buyer': is_buyer
        }
        return render(request, 'accounts/my_account/account.html', context)
class MyInfoView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/account_information.html')


class MySecurityView(View):
    def get(self, request):
        return render(request, 'accounts/my_account/security.html')


class MyPaymentView(View):
    def get(self, request):
        payment_info = PaymentInfo.objects.filter(customer=request.user)
        form = PaymentForm()
        return render(request, 'accounts/my_account/payment_methods.html', {'form': form})
    
    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Save payment information to session
            cardholder = form.cleaned_data['cardholder']
            cardnumber = form.cleaned_data['cardnumber']
            expiration_input = form.cleaned_data['expiration']
            cvv = form.cleaned_data['cvv']
            balance = form.cleaned_data['balance']
            is_default = form.cleaned_data['is_default']
            
            #converts the MM/YYYY input to YYYY/MM/DD for the DateField
            expiration_parts = expiration_input.split('/')
            expiration_date = datetime.date(int(expiration_parts[1]), int(expiration_parts[0]), int(1))

            # Create and save PaymentInfo object
            payment_info = PaymentInfo(
                cardholder=cardholder,
                cardnumber=cardnumber,
                expiration=expiration_date,
                cvv=cvv,
                balance=balance,
                is_default=is_default,
                customer=request.user  
            )
            payment_info.save()
            messages.success(request, "Payment method added successfully!") 

            # Check if the user wants to set this payment method as default
            if is_default:
                existing_default = PaymentInfo.objects.filter(customer=request.user, is_default=True).first()
                if existing_default:
                    existing_default.is_default = False
                    existing_default.save()
                payment_info.is_default = True
                payment_info.save()

            return render(request, 'accounts/my_account/payment_methods.html', {'form': form})
        else:
            # If form is invalid, re-render the form with errors
            messages.error(request, "Error in adding payment method. Please try again.")
            return render(request, 'accounts/my_account/payment_methods.html', {'form': form})
        

def edit_payment(request, payment_id):
    # Retrieve the PaymentInfo object from the database
    payment = PaymentInfo.objects.get(id=payment_id)
    
    # Process the request to edit payment information (e.g., update the payment object)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            # Redirect to a success page or back to the payment methods page
            messages.success(request, "Payment method updated successfully!")
            return render(request, 'accounts/my_account/payment_methods.html', {'form': form})
    else:
        # Render the form for editing payment information
        form = PaymentForm(instance=payment)
        return render(request, 'accounts/my_account/payment_methods.html', {'form': form})
    
    
class DeletePaymentView(View):
    def post(self, request, pk):
        payment = PaymentInfo.objects.get(pk=pk)
        payment.delete()
        return render(request, 'accounts/my_account/payment_methods.html', {'form': form})


class MyShippingView(View):
    def get(self, request):
        shipping_info = ShippingInfo.objects.filter(customer=request.user)
        form = ShippingForm()
        return render(request, 'accounts/my_account/shipping_methods.html', {'form': form})

    def post(self, request):
        form = ShippingForm(request.POST)
        if form.is_valid():
            # Save shipping information to session
            street = form.cleaned_data['street']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            country = form.cleaned_data['country']
            is_default = form.cleaned_data['is_default']

            # Create and save PaymentInfo object
            shipping_info = ShippingInfo(
                street=street,
                city=city,
                state=state,
                zipcode=zipcode,
                country=country,
                is_default=is_default,
                customer=request.user  # Assuming you have a user field in PaymentInfo model
            )
            shipping_info.save()
            messages.success(request, "Shipping address added successfully!") 

            if is_default:
                
                # If setting as default, check if there's already a default
                existing_default = ShippingInfo.objects.filter(customer=request.user, is_default=True).first()
                if existing_default:
                    existing_default.is_default = False
                    existing_default.save()
                shipping_info.is_default = True
                shipping_info.save()

            return render(request, 'accounts/my_account/shipping_methods.html', {'form': form})
        else:
            # If form is invalid, re-render the form with errors
            messages.error(request, "Error in adding shipping address. Please try again.")
            return render(request, 'accounts/my_account/shipping_methods.html', {'form': form})

def edit_shipping(request, shipping_id):
    # Retrieve the ShippingInfo object from the database
    shipping = ShippingInfo.objects.get(id=shipping_id)
    
    # Process the request to edit shipping information (e.g., update the shipping object)
    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            form.save()

            messages.success(request, "Shipping address updated successfully!")
            return render(request, 'accounts/my_account/shipping_methods.html', {'form': form})
    else:
        # Render the form for editing shipping information
        form = ShippingForm(instance=shipping)
        return render(request, 'accounts/my_account/shipping_methods.html', {'form': form})

class DeleteShippingView(View):
    def post(self, request, pk):
        shipping = ShippingInfo.objects.get(pk=pk)
        shipping.delete()
        return render(request, 'accounts/my_account/shipping_methods.html', {'form': form})


class MyOrdersView(View):
    def get(self, request):
        orders = Order.objects.filter(customer=request.user)
        context = {'orders': orders}
        return render(request, 'accounts/my_account/order_history.html', context)


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