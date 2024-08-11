from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart-detail'),
    path('checkout/', views.checkout_detail, name='checkout-detail'),
    path('orderitem/create/', views.add_to_cart, name='add-to-cart'),
    path('remove/<int:product_id>', views.cart_remove, name='cart-remove'),
    path('checkout/paid/<int:id>', views.checkout_paid, name='checkout-paid'),
    path('tracking/', views.tracking, name='tracking'),
]