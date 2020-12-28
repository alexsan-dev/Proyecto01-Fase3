from django import forms
from .models import *


class Transactions_Form(forms.ModelForm):

    class Meta:
        model = Transactions
        fields = ('amount', 'description')


class ThirdAccount_Form(forms.ModelForm):

    class Meta:
        model = Thirdaccount
        fields = ('id',)


class Spreads_Form(forms.ModelForm):

    class Meta:
        model = Spreadspay
        fields = ('employaccount', 'employname', 'amount', 'ismensualpayplan')
