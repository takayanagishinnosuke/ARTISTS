from distutils.command.upload import upload
from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# フォームクラス
class PostForm(forms.ModelForm):
  class Meta:
    model = Post #テーブル名
    fields = ('title',) #フィールド名
    #カラムにラベルを付けれるよ
    labels = {
      'title':'タイトル',
    }  