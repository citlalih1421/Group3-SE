from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from payments.models import PaymentInfo
from .models import Order
from django.contrib import messages
# Create your views here.

def get_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'orders/order.html', context)

class RefundView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        payment_info = PaymentInfo.objects.filter(customer=request.user, is_default=True).first()
        
        # Refund the customer's payment
        payment_info.balance += order.total
        payment_info.save()
        
        # Refund the sellers attached to order items
        for order_item in order.items.all():
            order_seller = order_item.shoe.seller
            seller_payment = PaymentInfo.objects.filter(customer=order_seller, is_default=True).first()
            seller_payment.balance -= order_item.total
            seller_payment.save()
        
        # Mark the order as refunded
        order.is_refunded = True
        order.save()
        
        messages.success(request, 'Order total has been successfully refunded to your default payment method and sellers.')
        return redirect('order', order_id=order_id)