from django.shortcuts import render

from .models import Order, OrderItem

def create_order(request):
    Order.objects.first()
