from decimal import Decimal
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
        print(str(order.total))
        # Refund the customer's payment
        buyer = request.user.userprofile
        print("Buyer Before: " + str(buyer.balance))
        buyer.balance += order.total
        buyer.save()
        print("Buyer After: " + str(buyer.balance))
        
        # Refund the sellers attached to order items
        for order_item in order.items.all():

            #refunds the money earned from the seller
            seller = order_item.shoe.seller.userprofile
            print("Seller Before: "+ str(seller.balance))
            seller.balance -= (order_item.total * order_item.quantity)
            seller.save()
            print("Seller After: " + str(seller.balance))
        
        # Mark the order as refunded
        order.is_refunded = True
        order.save()
        
        messages.success(request, 'Order total has been successfully refunded to your default payment method and sellers.')
        return redirect('order', order_id=order_id)