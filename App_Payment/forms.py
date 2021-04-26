from .models import BillingAddress
from django import forms


class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ('address','zipcode','city','country')