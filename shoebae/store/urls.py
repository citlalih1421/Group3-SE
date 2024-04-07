from django.urls import path
from django.conf.urls.static import static
from shoebae import settings
from .import views
from store.views import AddListingView, ViewAllListingsView, ProductPageView, DeleteListingView, ViewListingsView, Checkout


urlpatterns = [
    #empty for base url
    path('', ViewAllListingsView.as_view(), name="store"),
    path('cart/<int:cart_id>/', views.cart, name='cart'),
    path('add-to-cart/<slug:slug>/',views.add_to_cart,name='add_to_cart'),
    path('checkout/', Checkout.as_view(), name="checkout"),
    path('home/', views.home, name="home"),
    path('search/', views.search_view, name='search_view'),
    path('productpage/<slug:slug>/', ProductPageView.as_view(), name='productpage'),
    path('seller/', views.seller, name="seller"),
    path('seller/listing/', AddListingView.as_view(), name="listing" ),
    path('seller/listings/', ViewListingsView.as_view(), name="view_listings"),
    path('delete-listing/<slug:slug>/', DeleteListingView.as_view(), name='delete_listing'),
    path('fitler/', views.filter, name="filter"),
    path('testing/', views.testing, name="testing"),
    path('viewlisting/', views.viewlisting, name="viewlisting"),
]
