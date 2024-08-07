from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Order
from .cart import Cart
from .forms import OrderForm

def cart_detail(request):
    
    return render(request, 'cart/cart.html')


def checkout_detail(request):

    return render(request, 'cart/checkout.html')

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
        order = get_object_or_404(Order.objects.prefetch_related('items'), id=id)
        order.update(address=order_data['address'], city=order_data['city'], phone=order_data['phone'], note=order_data['note'])
        return redirect('payment:process')
        
    else:
        messages.error(request, f'Your Form is not Complect')
        redirect('cart:checkout-detail')
        