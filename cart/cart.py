from django.contrib import messages
from django.db.models.expressions import F

from .models import Order, OrderItem
from .forms import OrderItemForm

class Cart:
    
    def __init__(self, request):
        self.request = request
        
        user = self.request.user
        order = user.orders.filter(status='u').prefetch_related('items').first()
        
        if not order:
            order = Order.objects.create(name=user)

        self.order = order
    
    def add_order_item(self):
        form = OrderItemForm(self.request.POST)
        if form.is_valid():
            order_obj = form.save(commit=False)
            order_obj.order = self.order
            order_obj.save()
            
    def remove(self, product):
        orderitem = self.order.items.get(product_id=product.id)
        orderitem.delete()
        messages.success(self.request, 'Your product delete from the cart.')
        
    def add(self, product, quantity=1):
        orderitem = self.order.items.get(product_id=product.id)
        orderitem['quantity'] += quantity
        orderitem.save()
        messages.success(self.request, 'Your cart is update.')

    def show(self):
        return self.order.items.select_related('product', 'order').annotate(total_price_product = F('unit_price') * F('quantity'))
            
    def paid(self):
        self.order.status = 'p'
        self.order.save()
        messages.success(self.request, 'Your cart is paied.')
        
        
    def cancel(self):
        self.order.status = 'c'
        self.order.save()
        messages.success(self.request, 'Your cart is canceled.')
        
    def __len__(self):
        return sum([item.quantity for item in self.order.items.all()])
        
            
        