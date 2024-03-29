from django import forms

class ShippingForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=75)
    state = forms.CharField(max_length=50)
    zipcode = forms.CharField(max_length=10)
    number = forms.CharField(max_length=15)


class PaymentForm(forms.Form):
    cardholder = forms.CharField(max_length=100)
    cardnumber = forms.CharField(max_length=19)
    expiration = forms.CharField(max_length=5)
    ccv = forms.CharField(max_length=3)
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    zipcode = forms.CharField(max_length=10)
    number = forms.CharField(max_length=15)
