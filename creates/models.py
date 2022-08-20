from distutils.command.upload import upload
from django.db import models

#---DBモデルの定義---#
class Post(models.Model):
  title = models.CharField(max_length=100)
  published = models.DateTimeField()
  image = models.ImageField(blank=True)
  image_two = models.ImageField(blank=True)
  image_three = models.ImageField(blank=True)
  image_four = models.ImageField(blank=True)
  
