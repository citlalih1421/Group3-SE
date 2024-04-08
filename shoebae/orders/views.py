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
        payment_info.balance += order.total
        payment_info.save()
        order.is_refunded = True
        order.save()
        messages.success(request, 'Order total has successfully been refunded to your default payment method')
        return redirect('order', order_id=order_id)