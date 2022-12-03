from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.blog_list),
    path('blog/<int:id>', views.blog_detail),
    path('share/<int:id>', views.share_blog),
    path('comment', views.comment),
    path('like', views.like)
]
