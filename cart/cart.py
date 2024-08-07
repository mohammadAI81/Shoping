from django.contrib import messages
from django.db.models.expressions import F

from .models import Order
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
            cleaned_data = form.cleaned_data
            orderitem = self.order.items.filter(product_id=cleaned_data['product'].id)
            if orderitem.exists():
                orderitem.update(quantity=cleaned_data['quantity'])
                messages.success(self.request, 'Your order is Update.')
            else:
                order_obj = form.save(commit=False)
                order_obj.order = self.order
                order_obj.save()
                messages.success(self.request, 'Your order is submitted.')
            return
        messages.error(self.request, 'Your order is not submit')
            
    def remove(self, id:int):
        orderitem = self.order.items.get(product_id=id)
        orderitem.delete()
        messages.success(self.request, 'Your product is deleted from the cart.')
        
    def add(self, id:int, quantity:int =1):
        orderitem = self.order.items.get(product_id=id)
        orderitem.quantity += quantity
        orderitem.save()
        messages.success(self.request, 'Your cart is updated.')
            
    def paid(self):
        self.order.status = 'p'
        self.order.save()
        messages.success(self.request, 'Your cart is paid.')
        
    def cancel(self):
        self.order.status = 'c'
        self.order.save()
        messages.success(self.request, 'Your cart is canceled.')
        
    def __iter__(self):
        for item in self.order.items.select_related('product', 'order').annotate(total_price_product=F('unit_price') * F('quantity')):
            yield item
    
    def __len__(self):
        return sum(item.quantity for item in self.order.items.all())
