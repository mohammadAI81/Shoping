from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

from .models import Order
from .cart import Cart
from .forms import OrderForm


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


def checkout_detail(request):
    cart = Cart(request)
    return render(request, 'cart/checkout.html', {'cart': cart})


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart:cart-detail')


@require_POST
@login_required(login_url='/account/login/')
def add_to_cart(request):
    cart = Cart(request)
    cart.add_order_item()
        
    return redirect('store:products')


@require_POST
@login_required(login_url='/account/login/')
def checkout_paid(request, id):
    form = OrderForm(request.POST)
    
    if form.is_valid():
        order_data = form.cleaned_data
        order = get_object_or_404(Order, id=id)
        order.address=order_data['address']
        order.city=order_data['city']
        order.phone=order_data['phone']
        order.note=order_data['note']
        order.save()
        return redirect('payment:process')
        
    else:
        messages.error(request, f'Your Form is not Complect')
        redirect('cart:checkout-detail')
        
        
def tracking(request):
    if request.method == 'POST':
        ref_if = request.POST['order']
        email = request.POST['email']
        get_object_or_404(get_user_model(), email=email)
        return redirect('payment:info-payment', ref_if)
    return render(request, 'cart/tracking.html')