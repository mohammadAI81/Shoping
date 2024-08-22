from django.db.models import Count
from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'city', 'num_items', 'status')
    list_editable = ('status', )
    search_fields = ('name', )
    list_filter = ('status', )
    list_select_related = ('name', )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items').annotate(count_items=Count('items'))

    @admin.display(ordering='count_items', description='# Items')
    def num_items(self, product):
        return product.count_items
    
    
@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    list_display = ('product', 'unit_price', 'quantity', )
    list_editable = ('quantity', )
    search_fields = ('product', 'quantity', )
    list_select_related = ('product', 'order', )
    autocomplete_fields = ('product', )
    
