from django.urls import path
from django.contrib.auth import views
from . import views

urlpatterns = [
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('account/', views.MyAccountView, name='account'),
    path('account/account-information/', views.MyInfoView, name='account_information'),
    path('account/security/', views.MySecurityView, name='account_security'),
    path('account/payment-methods/', views.MyPaymentView, name='payment_methods'),
    path('account/shipping-methods/', views.MyShippingView, name='shipping_methods'),
    path('account/order-history/', views.MyOrdersView, name='order_history'),
    path('account/tickets/', views.MyTicketsView, name='tickets'),
    #path('account/my-listings/', views.MyListingsView, name='my_listings'),
]