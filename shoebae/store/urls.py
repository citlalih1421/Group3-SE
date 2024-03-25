from django.urls import path
from . import views
from .views import AddListingView
from .views import ViewListingsView

urlpatterns = [
    #empty for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('home/', views.home, name="home"),
    path('productpage/', views.productpage, name="productpage"),
    path('seller/', views.seller, name="seller"),
    path('seller/listing/', AddListingView.as_view(), name="listing" ),
    path('seller/listings/', ViewListingsView.as_view(), name="view_listings"),

]




