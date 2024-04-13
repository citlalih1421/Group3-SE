from django import forms

class ShippingForm(forms.Form):
    street = forms.CharField(max_length=100)
    city = forms.CharField(max_length=75)
    state = forms.CharField(max_length=50)
    zipcode = forms.CharField(max_length=10)
    country = forms.CharField(max_length=75)
    is_default = forms.BooleanField(label='Set as default shipping method', required=False)


class PaymentForm(forms.Form):
    cardholder = forms.CharField(max_length=100)
    cardnumber = forms.CharField(max_length=19)
    expiration = forms.CharField(max_length=7, label='Expiration (MM/YYYY)')
    cvv = forms.CharField(max_length=4, label='CVV')
    balance = forms.IntegerField(min_value=0, max_value=10000)
    is_default = forms.BooleanField(label='Set as default payment method', required=False)
    
