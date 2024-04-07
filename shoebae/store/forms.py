from django import forms
from .models import Shoe, Condition, Category, Brand

class ShoeForm(forms.ModelForm):
    size = forms.DecimalField(max_digits=3, decimal_places=1, widget=forms.NumberInput(attrs={'step': '0.5'}))
    
    class Meta:
        model = Shoe
        fields = ['name', 'image', 'quantity', 'price', 'size', 'condition', 'brand', 'category']
        error_messages = {
            'name': {'required': "Please enter the name of the shoe."},
            'image': {'required': "Please upload an image of the shoe."},
            'quantity': {'required': "Please enter the quantity of the shoe."},
            'price': {'required': "Please enter the price of the shoe."},
            'size': {'required': "Please enter the size of the shoe."},
            'conditions': {'required': "Please specify the condition of the shoe."},
            'brand': {'required': "Please enter the brand of the shoe."},
            'category': {'required': "Please enter the category of the shoe."},
        }
    def __init__(self, *args, **kwargs):
        super(ShoeForm, self).__init__(*args, **kwargs)
        self.fields['condition'].queryset = Condition.objects.all()
        self.fields['category'].queryset = Category.objects.all()
        self.fields['brand'].queryset = Brand.objects.all()

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, required=False)