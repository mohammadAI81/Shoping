from django.urls import path,include

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.list_product_category, name='products'),
    # path('like/<int:product_id>/', views.like_product, name='like'),
    path('<slug:slug>/', views.DetailProduct.as_view(), name='product'),
]
