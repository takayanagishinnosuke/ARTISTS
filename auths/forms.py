from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from .models import Account

class AccountForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput(),label='パスワード')
  class Meta():
    model = User
    fields = ['username','email','password']
    labels = {'username':'ユーザーID','email':'メール'}
    
class AddAccountForm(forms.ModelForm):
  class Meta():
    model = Account
    fields = ['nickname']
    labels = {'nickname':'ニックネーム'}