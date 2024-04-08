from django.urls import path
from . import views

urlpatterns = [
    path('order/<int:order_id>/', views.get_order, name="order"),
    path('order/<int:order_id>/refund/', views.RefundView.as_view(), name='refund_submit')
]