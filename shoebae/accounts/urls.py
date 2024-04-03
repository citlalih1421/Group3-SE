from django.urls import path
from . import views
from accounts.views import MyPaymentView,MyShippingView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('account/', views.MyAccountView.as_view(), name='account'),
    path('account/account-information/', views.MyInfoView.as_view(), name='account_information'),
    path('account/security/', views.MySecurityView.as_view(), name='account_security'),
    path('account/payment-methods/', MyPaymentView.as_view(), name='payment_methods'),
    path('account/shipping-methods/', MyShippingView.as_view(), name='shipping_methods'),
    path('account/order-history/', views.MyOrdersView.as_view(), name='order_history'),
    path('account/tickets/', views.MyTicketsView.as_view(), name='tickets'),
    path('account/favorites/', views.MyFavoritesView.as_view(), name='favorites'),
    # path('account/my-listings/', views.MyListingsView.as_view(), name='my_listings'),
]
