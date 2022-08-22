from email.mime import image
from urllib import request
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


def index(request):
  # Postテーブルから更新の昇順で取得Query
  posts = Post.objects.order_by('-published')
  # index.htmlにposts(データを渡す)
  return render(request,'posts/index.html', {'posts':posts})

# 新規投稿の処理
def new_create(request):
  if request.method == 'POST':
    # postされたformを受け取る。
    form = forms.PostForm(request.POST, request.FILES)
    # formのバリデーション
    if form.is_valid(): 
      post = form.save(commit=False) # 引数のcommit=False <-まだcommitはしないよという事
      post.published = dt.now()  #publishedは今の時刻に

      word = art_create.deepL(post.title)
      filepath_list = art_create.create_art(word)
      post.image = filepath_list[0]
      post.image_two = filepath_list[1]
      post.image_three = filepath_list[2]
      post.image_four = filepath_list[3]
      post.save()
      return redirect('/creates') #URLで指定
  else:
    form = forms.PostForm() #formの再描画

  return render(request, 'posts/new_create.html', {'form': form})

#詳細確認画面へ
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