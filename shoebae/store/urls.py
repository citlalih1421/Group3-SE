from django.urls import path
from . import views
urlpatterns = [
    #empty for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('home/', views.home, name="home"),
    path('addlisting/', views.addlisiting, name="addlisting"),
    path('productpage/', views.productpage, name="productpage"),
    path('seller/', views.seller, name="seller"),
    path('apply/', views.apply, name="apply"),
    path('testing/', views.testing, name="testing"),
    path('listings/', views.filter, name="listings"),
]