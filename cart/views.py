from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Order, OrderItem
from .cart import Cart

def cart_detail(request):
    context = {
           
    }
    return render(request, 'cart/cart.html', context)

@require_POST
@login_required(login_url='/account/login/')
def add_to_cart(request):
    cart = Cart(request)
    if cart.add_order_item():
        messages.success(request, 'Your order is submit')
    else:
        messages.error(request, 'Your order is not submit')
    return redirect('store:products')
        
@login_required(login_url='/account/login/')
def checkout(request):
    cart = Cart(request)
    cart.paid()
    return redirect('page:home')