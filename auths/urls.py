from django.urls import path
from . import views

# app_name = 'auths'

urlpatterns = [
  path('register', views.AccountRegistration.as_view(), name='register'),
  path('', views.Login, name='Login'),
  path('logout', views.Logout, name='Logout'),
]