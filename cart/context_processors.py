from django.db.models.aggregates import Sum

from .models import Order

def cart(request):
    if request.user.is_authenticated:
        num_product =  Order.objects.filter(status=Order.STATUS_ORDER[0][0], name=request.user) \
                                            .aggregate(count=Sum('items__quantity'))
        if num_product['count'] is None:
            num_product['count'] = 0
        return {'count_quantity': num_product.get('count')}
    else:
        return {'count_quantity': 0}