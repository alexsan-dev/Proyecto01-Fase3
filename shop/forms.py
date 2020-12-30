from django import forms
from .models import *


class Purchases_Form(forms.ModelForm):

    class Meta:
        model = Purchases
        fields = ('description', 'amount', 'isdollar')
