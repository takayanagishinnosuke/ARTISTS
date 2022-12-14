from email.mime import image
from unittest import result
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
from .art_create import deepL, create_art, create_art2
import os
from dotenv import load_dotenv
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.decorators import login_required
from django_celery_results.models import TaskResult


load_dotenv()
# AWS S3の環境変数を読み込み
accesskey = os.getenv('ACCESSkEY')
secretkey = os.getenv('SECRETkEY')
region = 'ap-northeast-1'

# TOP画面、loginのuser_idと一致している絵画データを羅列
@login_required
def index(request):
  user_id = request.user.id
  # fileパスが空のレコードを取得
  fileobj = Post.objects.filter(image="")
  for i in fileobj:
    # task_idを格納
    task_id = i.task_id
  try:
    # TaskResultからid一致しているレコード取得して
    result_object = TaskResult.objects.get(task_id=task_id)
    # 処理完了&成功してたら
    if result_object.status == "SUCCESS":
      # 画像のファイルパスを取得して
      file_path = eval(result_object.result)
      i.image = file_path[0]
      i.image_two = file_path[1]
      i.image_three = file_path[2]
      i.image_four = file_path[3]
      i.save()
  except:
    print('Error')
  
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
      word = deepL(post.title)
      print(word) #英語翻訳確認
      if num ==1:
        #repreecateで絵画生成
        user_id = str(request.user.id)
        #非同期処理でバックグラウンドでは知らせる
        filepath_list = create_art.delay(word,user_id)        
        post.task_id = filepath_list.id
        post.save()
        
      elif num ==2:
        user_id = str(request.user.id)
        #非同期処理でバックグラウンドでは知らせる
        filepath_list = create_art2.delay(word,user_id)        
        post.task_id = filepath_list.id
        post.save()
                
      return redirect('/creates') #URLで指定
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
  BUCKET_NAME = 'artists.media'
  record = get_object_or_404(Post,id=art_id)
  path1 = str(record.image)
  path2 = str(record.image_two)
  path3 = str(record.image_three)
  path4 = str(record.image_four)
  delete_list = [path1,path2,path3,path4]
  record.delete()
  
  #s3の保存データを消す
  # s3 = boto3.client('s3',aws_access_key_id=accesskey,
  #                   aws_secret_access_key=secretkey,
  #                   region_name=region)
  # for path in delete_list:
  #   try:
  #     s3.delete_object(Bucket=BUCKET_NAME,Key=path)
  #   except:  
  #     print('削除OK')
    
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
    
    s3 = boto3.client('s3',aws_access_key_id=accesskey,
                      aws_secret_access_key=secretkey,
                      region_name=region)
    from_bucket = 'artists.media'
    filename = filepath
    bucket_name = 'artists.img'
    CopySource= os.path.join(from_bucket,filename)
    #バケットを移動する処理
    s3.copy_object(Bucket=bucket_name,CopySource=CopySource,Key=filename,)
    print('copy ok')
  
  return redirect('posts:index')
    
  