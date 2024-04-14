from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.list_product_category, name='products'),
    path('like/<int:product_id>/', views.likend, name='like'),
    path('<slug:slug>/', views.DetailProduct.as_view(), name='product'),
]
