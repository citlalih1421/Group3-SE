from django.urls import path
from django.conf.urls.static import static
from shoebae import settings
from .import views
from .views import AddListingView, ProductPageView
from .views import ViewListingsView
from store.views import AddListingView, ShoeSearchListView, ViewAllListingsView
from .views import DeleteListingView

urlpatterns = [
    #empty for base url
    path('', ViewAllListingsView.as_view(), name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('home/', views.home, name="home"),
    path('productpage/<slug:slug>/', ProductPageView.as_view(), name='productpage'),
    path('seller/', views.seller, name="seller"),
    path('seller/listing/', AddListingView.as_view(), name="listing" ),
    path('seller/listings/', ViewListingsView.as_view(), name="view_listings"),
    path('store/search/', ShoeSearchListView.as_view(), name='search'),
    path('listing/delete/<slug:slug>/', DeleteListingView.as_view(), name='delete_listing'),
    path('fitler/', views.filter, name="filter"),
    path('testing/', views.testing, name="testing"),
    path('viewlisting/', views.viewlisting, name="viewlisting"),
]
