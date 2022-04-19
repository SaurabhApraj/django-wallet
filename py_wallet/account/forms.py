from django import forms
from account.models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class AddRemoveBalanceForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['balance']