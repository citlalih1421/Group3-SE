from django.urls import path
from . import views
urlpatterns = [
    #empty for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('home/', views.home, name="home"),
    path('productpage/', views.productPage, name="productpage"),
    path('seller/', views.seller, name="seller"),
    path('seller/listing', views.add_listing, name="listing" )
]