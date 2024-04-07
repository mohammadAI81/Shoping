from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.ListProductCategory, name='products'),
    path('<slug:slug>/', views.DetailProduct.as_view(), name='product'),
]
