from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('<slug:slug>/', views.detail_blog, name='blog'),
    path('<slug:slug>/comment/create/', views.create_comment, name='create-comment'),
    path('<slug:slug>/comment/reply/create/', views.create_reply_comment, name='create-reply-comment'),
]
