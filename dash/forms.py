from django import forms
from .models import *


class Account_Form(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('isdollar', )


class SingleUser_Form(forms.ModelForm):

    class Meta:
        model = Singleuser
        fields = ('cui', 'nit', 'name', 'username', 'password', 'phone')


class BusinessUser_Form(forms.ModelForm):

    class Meta:
        model = Businessuser
        fields = ('comercialname', 'name', 'agent', 'phone')


class Checks_Form(forms.ModelForm):

    class Meta:
        model = Accountcheck
        fields = ('name', 'amount')


class Charge_Change_Form(forms.ModelForm):

    class Meta:
        model = Accountcheck
        fields = ('name',)
