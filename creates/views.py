from django.shortcuts import render, get_object_or_404, redirect 
#get_object_or_404 -> ojectが無い時に404を返す関数
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from datetime import datetime as dt
from pathlib import Path
import boto3
from io import BytesIO
from PIL import Image
import numpy as np
from . import forms
from . import art_create


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

def detail(request,art_id):
  arts = Post.objects.get(id=art_id)
  
  print(arts)
  return render(request,'posts/detail.html',{'arts':arts})
