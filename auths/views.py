from django.shortcuts import render, redirect
from django.views.generic import TemplateView # テンプレートタグ
from .forms import AccountForm, AddAccountForm # ユーザーアカウントフォーム
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse 
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from creates import views

#新規登録
class  AccountRegistration(TemplateView):
  def __init__(self):
    self.params = {
      'AccountCreate':False,
      'account_form':AccountForm(),
      'add_account_form':AddAccountForm()
    }
    
  def get(self,request):
    self.params['account_form'] = AccountForm()
    self.params['add_account_form'] = AddAccountForm()
    self.params['AccountCreate'] = False
    return render(request,'auth/register.html',context=self.params)
  
  def post(self,request):
    self.params['account_form'] = AccountForm(data=request.POST)
    self.params['add_account_form'] = AddAccountForm(data=request.POST)
    
    if self.params['account_form'].is_valid() and self.params['add_account_form'].is_valid():
      # アカウント情報をDB保存
      account = self.params["account_form"].save()
      # パスワードをハッシュ化
      account.set_password(account.password)
      # ハッシュ化パスワード更新
      account.save()
      # 下記追加情報
      # 下記操作のため、コミットなし
      add_account = self.params["add_account_form"].save(commit=False)
      # AccountForm & AddAccountForm 1vs1 紐付け
      add_account.user = account
      add_account.save()
      
      #アカウント作成情報更新
      self.params['AccountCreate'] = True
      
    else:
      print(self.params['account_form'].errors)
    
    return render(request,'auth/register.html',context=self.params)

#ログイン
def Login(request):
  if request.method == 'POST':
    Id = request.POST.get('userid')
    Pass = request.POST.get('password')
    
    #Djangon認識
    user = authenticate(username=Id,password=Pass)
    
    #ユーザー認証
    if user:
      #ユーザーアクティベート機能
      if user.is_active:
        login(request,user)
        return redirect('/creates/')
      else:
        #アカウント利用不可
        return HttpResponse('アカウントが有効ではありません')
    else:
      return HttpResponse('ログインIDまたはパスワードが間違ってます')
  #GETのとき
  else:
    return render(request, 'auth/login.html')

#ログアウト
@login_required
def Logout(request):
  logout(request)
  #ログイン画面遷移
  return HttpResponseRedirect(reverse('auths:Login'))
