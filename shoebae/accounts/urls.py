from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('account/account-information/', views.account_information_view, name='account_information'),
    path('account/security/', views.security_view, name='account_security'),
    path('account/payment-methods/', views.payment_methods_view, name='payment_methods'),
    path('account/shipping-methods/', views.shipping_methods_view, name='shipping_methods'),
    path('account/order-history/', views.order_history_view, name='order_history'),
    path('account/tickets/', views.tickets_view, name='tickets')
]