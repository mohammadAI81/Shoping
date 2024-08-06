from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseNotFound

from .models import Order, OrderItem
from .cart import Cart
from .forms import OrderForm

def cart_detail(request):
    
    return render(request, 'cart/cart.html')


def checkout_detail(request):

    return render(request, 'cart/checkout.html')

@require_POST
@login_required(login_url='/account/login/')
def add_to_cart(request):
    cart = Cart(request)
    if cart.add_order_item():
        pass
    else:
        messages.error(request, 'Your order is not submit')
    return redirect('store:products')

@require_POST
@login_required(login_url='/account/login/')
def checkout_paid(request, id):
    form = OrderForm(request.POST)
    if form.is_valid():
        order_data = form.cleaned_data
        order = Order.objects.prefetch_related('items').filter(id=id)
        if order.exists():
            order.update(address=order_data['address'], city=order_data['city'], phone=order_data['phone'], note=order_data['note'])
            return redirect('payment:process')
        else:
            return HttpResponseNotFound('Not Found')
    else:
        messages.error(request, f'Your Form is not Complect')
        redirect('cart:checkout-detail')
        