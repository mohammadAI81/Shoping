from django.db.models.aggregates import Count

from .models import Order

def cart(request):
    if request.user.is_authenticated:
        return {'cart': Order.objects.aggregate(count=Count('items'))}
    else:
        return {'cart': {'count': 0}}