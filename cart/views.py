from django.shortcuts import render

from .models import Order, OrderItem
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    context = {
           
    }
    return render(request, 'cart/cart.html', context)
