from django.urls import path
from . import views
urlpatterns = [
    #empty for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('home/', views.home, name="home"),
    path('addisting/', views.addLisiting, name="addlisting"),
    path('productpage/', views.productPage, name="productpage"),
    path('seller/', views.seller, name="seller"),
]