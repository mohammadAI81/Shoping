from django import forms

from .models import Order, OrderItem

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'unit_price', 'quantity']
        
        
class OrderForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(), required=False)
    
    
    class Meta:
        model = Order
        fields = ['address', 'phone', 'city', 'note']
        
        