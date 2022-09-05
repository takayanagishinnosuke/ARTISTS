from urllib import request
from dotenv import load_dotenv
import os
import replicate
import requests
import json
import io
import sys
import pandas as pd
from pandas import json_normalize
import datetime
from urllib import request
from .models import Post
from celery import shared_task
import boto3

load_dotenv()
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
API_KEY = os.getenv('API_KEY')

# AWS S3の環境変数を読み込み
accesskey = os.getenv('ACCESSkEY')
secretkey = os.getenv('SECRETkEY')
region = 'ap-northeast-1'
bucket_name = 'artists.media'

#モデル1のときに呼び出す関数
@shared_task
def create_art(trance_title,user_id):
  dt_now = datetime.datetime.now()
  dt_now_fmt = dt_now.isoformat()
  
  model = replicate.models.get("afiaka87/retrieval-augmented-diffusion")
  img_lists = model.predict(number_of_variations=8,prompts=trance_title)
    
  img_list = []
  file_name_list = []
  id = user_id
  
  for list_item in img_lists:
    img_list.append(list_item['image'])

  for i in img_list[4:]:
    img = i
    print(i)
    filename = id+'_'+dt_now_fmt + i[-12:]
    file_path = 'media/' + id + '_' + dt_now_fmt + i[-12:]
    file_name_list.append(filename)
    res = requests.get(img)
    images = res.content
    with open(file_path,'wb') as f:
      f.write(images)
    #S3にアップ
    s3 = boto3.client('s3',aws_access_key_id=accesskey,
                      aws_secret_access_key=secretkey,
                      region_name=region)
    s3.upload_file(file_path,bucket_name,filename)
    print('upload完了')
    #ローカルのファイルは消す
    os.remove(file_path)
      
  return file_name_list 

#モデル2を選択した際に呼び出す関数
@shared_task
def create_art2(trance_title,user_id):
  dt_now = datetime.datetime.now()
  dt_now_fmt = dt_now.isoformat()
  model = replicate.models.get("borisdayma/dalle-mini")
  img_lists = model.predict(n_predictions=8,prompt=trance_title)
  
  img_list = []
  file_name_list = []
  id = user_id
  
  for list_item in img_lists:
    img_list.append(list_item['image'])

  for i in img_list[4:]:
    img = i
    print(i)
    filename = id+'_'+dt_now_fmt + i[-12:]
    file_path = 'media/' + id + '_' + dt_now_fmt + i[-12:]
    file_name_list.append(filename)
    res = requests.get(img)
    images = res.content
    with open(file_path,'wb') as f:
      f.write(images)
    #S3にアップ
    s3 = boto3.client('s3',aws_access_key_id=accesskey,
                  aws_secret_access_key=secretkey,
                  region_name=region)
    s3.upload_file(file_path,bucket_name,filename)
    print('upload完了')
    #ローカルのファイルは消す
    os.remove(file_path)
      
  return file_name_list

#DeepL_APIの処理(翻訳して返す)
def deepL(inputtext):
  text =  inputtext
  source_lang = 'JA'
  target_lang = 'EN'

  # パラメータの指定
  params = {
              'auth_key' : API_KEY,
              'text' : text,
              'source_lang' : source_lang, # 翻訳対象の言語
              "target_lang": target_lang  # 翻訳後の言語
          }

  # リクエストを投げる
  request = requests.post("https://api-free.deepl.com/v2/translate", data=params) # URIは有償版, 無償版で異なるため要注意
  result = request.json()
  
  df = json_normalize(result['translations'])
  trance_text = df.at[0,'text']

  return trance_text