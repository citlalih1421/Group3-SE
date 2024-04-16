
import datetime
from django import forms
from payments.models import PaymentInfo

class ShippingForm(forms.Form):
    street = forms.CharField(max_length=100)
    city = forms.CharField(max_length=75)
    state = forms.CharField(max_length=50)
    zipcode = forms.CharField(max_length=10)
    country = forms.CharField(max_length=75)
    is_default = forms.BooleanField(label='Set as default shipping method', required=False)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = ['cardholder', 'cardnumber', 'expiration', 'cvv', 'balance', 'is_default']
        widgets = {
            'expiration': forms.DateInput(attrs={'type': 'date'})
        }
    
