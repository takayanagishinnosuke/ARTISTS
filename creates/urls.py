from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'posts' 

urlpatterns = [
    path('', views.index, name='index'),
    path('new_create',views.new_create,name='new_create'),
    path('<int:art_id>',views.detail, name='detail'),
    path('delete/<int:art_id>',views.delete, name='delete'),
    path('upload/<int:pk>',views.upload, name='upload' ),
]

