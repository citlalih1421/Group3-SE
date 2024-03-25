from django.urls import path
from . import views
from store.views import AddListingView, ShoeSearchListView

urlpatterns = [
    #empty for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('home/', views.home, name="home"),
    path('productpage/', views.productpage, name="productpage"),
    path('seller/', views.seller, name="seller"),
    path('seller/listing/', AddListingView.as_view(), name="listing" ),
    path('store/search/', ShoeSearchListView.as_view(), name='search')
]