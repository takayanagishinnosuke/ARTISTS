from email.mime import image
from urllib import request
from venv import create
from django.shortcuts import render, get_object_or_404, redirect 
#get_object_or_404 -> ojectが無い時に404を返す関数
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from .models import Post
from datetime import datetime as dt
from pathlib import Path
import boto3
from io import BytesIO
from PIL import Image
import numpy as np
from . import forms
from . import art_create
import os
from dotenv import load_dotenv
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.decorators import login_required

load_dotenv()

# TOP画面、loginのuser_idと一致している絵画データを羅列
@login_required
def index(request):
  user_id = request.user.id
  # Postテーブルから更新の昇順で取得Query
  posts = Post.objects.filter(user_id=user_id).order_by('-published')
  # index.htmlにposts(データを渡す)
  return render(request,'posts/index.html', {'posts':posts})

# 新規投稿の処理
@login_required
def new_create(request):
  if request.method == 'POST':
    # postされたformを受け取る。
    form = forms.PostForm(request.POST, request.FILES)
    num = int(request.POST['radio'])
    
    # formのバリデーション
    if form.is_valid(): 
      post = form.save(commit=False) # 引数のcommit=False <-まだcommitはしないよという事
      post.published = dt.now()  #publishedは今の時刻に
      post.user_id = request.user.id
      #Deeplの呼び出し
      word = art_create.deepL(post.title)
      print(word) #英語翻訳確認
      
      if num ==1:
        #repreecateで絵画生成
        user_id = str(request.user.id)
        filepath_list = art_create.create_art(word,user_id)
        #filepath_listからファイルパスを取得して
        post.image = filepath_list[0]
        post.image_two = filepath_list[1]
        post.image_three = filepath_list[2]
        post.image_four = filepath_list[3]
        post.save() #保存
        return redirect('/creates') #URLで指定
      
      elif num ==2:
        user_id = str(request.user.id)
        filepath_list = art_create.create_art2(word,user_id)
        #filepath_listからファイルパスを取得して
        post.image = filepath_list[0]
        post.image_two = filepath_list[1]
        post.image_three = filepath_list[2]
        post.image_four = filepath_list[3]
        post.save() #保存
        
        return redirect('/creates') 
  else:
    form = forms.PostForm() #formの再描画

  return render(request, 'posts/new_create.html', {'form': form})

#詳細確認画面へ
@login_required
def detail(request,art_id):
  arts = Post.objects.get(id=art_id)
  return render(request,'posts/detail.html',{'arts':arts})

#削除の処理
@require_POST
def delete(request,art_id):
  record = get_object_or_404(Post,id=art_id)
  path1 = 'media/' + str(record.image)
  path2 = 'media/' + str(record.image_two)
  path3 = 'media/' + str(record.image_three)
  path4 = 'media/' + str(record.image_four)
  os.remove(path1)
  os.remove(path2)
  os.remove(path3)
  os.remove(path4)
  record.delete()
  return redirect('posts:index')

#UPLOADの処理
def upload(request,pk):
  if request.method=="POST":
    record = get_object_or_404(Post,id=pk)
    filepath = ''
    if "upload1" in request.POST:
      filepath = str(record.image)
    elif "upload2" in request.POST:
      filepath = str(record.image_two)
    elif "upload3" in request.POST:
      filepath = str(record.image_three)
    elif "upload4" in request.POST:
      filepath = str(record.image_four)
    
    accesskey = os.getenv('ACCESSkEY')
    secretkey = os.getenv('SECRETkEY')
    region = 'ap-northeast-1'
    s3 = boto3.client('s3',aws_access_key_id=accesskey,
                      aws_secret_access_key=secretkey,
                      region_name=region)
    imgpath = f'media/{filepath}'
    filename = filepath
    bucket_name = 'artists.img'
    
    s3.upload_file(imgpath,bucket_name,filename)
    print('upload ok')
  
  return redirect('posts:index')
    
  