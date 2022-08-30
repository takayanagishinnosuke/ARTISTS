from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

#---DBモデルの定義---#
class Post(models.Model):
  title = models.CharField(max_length=100,null=False)
  published = models.DateTimeField(null=False)
  image = models.ImageField(blank=True)
  image_two = models.ImageField(blank=True)
  image_three = models.ImageField(blank=True)
  image_four = models.ImageField(blank=True)
  user_id = models.IntegerField(null=True,blank=True)
  task_id = models.CharField(max_length=100,null=True,blank=True)
  
