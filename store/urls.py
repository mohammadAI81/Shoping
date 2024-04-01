from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.ListProductCategory.as_view(), name='products'),
]