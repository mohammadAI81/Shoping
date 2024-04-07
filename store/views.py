from django.shortcuts import render
from django.db.models import Count, Q
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator

from .models import Category, Like, Color, Comment, Product, Brand
from .variable import SHOW, SORT


def ListProductCategory(request):
    products = Product.objects.select_related('category', 'color', 'brand')
    request_get = request.GET

    # For Filter
    if sort := request_get.get('sort'):
        products = products.order_by(sort)

    category = request_get.get('category')
    brand = request_get.get('brand')
    color = request_get.get('color')
    if category or brand or color:
        q_objects = Q()
        if category:
            q_objects |= Q(category__name=category)
        if brand:
            q_objects &= Q(brand__name=brand)
        if color:
            q_objects &= Q(color__name=color)
        products = products.filter(q_objects)
    
    context = {'products': products}
    
    # Pagination
    context['num'] = request_get.get('page_num')   
    page_num = request_get.get('page')
    if context['num'] is None:
        context['num'] = request_get.get('num')
    if page_num or context['num']:
        if context['num'] != 'All':
            paginator = Paginator(products, context['num'])
            products = paginator.get_page(page_num)
            context['page_obj'] = products

    
    context['products'] = products
    
    # For Sort & Show Num Paginator
    context['sorts'] = SORT
    context['shows'] = SHOW

    # Count Of Category & Brand & Color
    context['categories'] = Category.objects.all().annotate(num_product=Count('product'))
    context['brands'] = Brand.objects.all().annotate(num_product=Count('product'))
    context['colors'] = Color.objects.all().annotate(num_product=Count('product'))
    context['values'] = request_get

    return render(request, 'store/products.html', context) 


class DetailProduct(DetailView):
    queryset = Product.objects.select_related('category', 'brand', 'color')
    template_name = 'store/product.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_like'] = context['product'].likes.count()
        return context
