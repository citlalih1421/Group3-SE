from django.urls import path
from . import views
<<<<<<< HEAD
from .views import AddListingView
from .views import ViewListingsView
=======
from store.views import AddListingView, ShoeSearchListView
>>>>>>> f7e592c67c1700be4e40ddf98f41f5b0923a4461

urlpatterns = [
    #empty for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('home/', views.home, name="home"),
    path('productpage/', views.productpage, name="productpage"),
    path('seller/', views.seller, name="seller"),
    path('seller/listing/', AddListingView.as_view(), name="listing" ),
<<<<<<< HEAD
    path('seller/listings/', ViewListingsView.as_view(), name="view_listings"),

]




=======
    path('store/search/', ShoeSearchListView.as_view(), name='search')
]
>>>>>>> f7e592c67c1700be4e40ddf98f41f5b0923a4461
