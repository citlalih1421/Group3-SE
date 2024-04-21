
import datetime
from django import forms
from orders.models import ShippingInfo
from payments.models import PaymentInfo

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ['street','city','state','zipcode','country','is_default']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = ['cardholder', 'cardnumber', 'expiration', 'cvv', 'is_default']
        widgets = {
            'expiration': forms.DateInput(attrs={'type': 'date'})
        }
    
