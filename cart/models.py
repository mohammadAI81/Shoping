from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

from store.models import Product


class SortByDateTimeManage(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-datetime_created')


class Order(models.Model):
    STATUS_ORDER = [
        ('u', 'Unpaid'),
        ('p', 'paid'),
        ('c', 'Canceled')
    ]

    name = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='orders')
    address = models.CharField(max_length=550, blank=True)
    city = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_ORDER, default=STATUS_ORDER[0][0])
    
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modifild = models.DateTimeField(auto_now=True)
    
    objects = SortByDateTimeManage()
    
    def __str__(self):
        return self.name.username
    
    def get_total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += item.quantity * item.unit_price
        return total_price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.product} -> {self.quantity}'
