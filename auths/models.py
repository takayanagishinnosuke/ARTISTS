from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  # 追加フィールド
  nickname = models.CharField(max_length=20)
