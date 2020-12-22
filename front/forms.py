from django import forms
from .models import *


class transactions(forms.ModelForm):

    class Meta:
        model = Transactions
        fields = ('amount', 'description')
