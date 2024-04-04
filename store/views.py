from django.shortcuts import render
from django.db.models import Count
from django.views.generic import ListView, DetailView

from .models import Category, Like, Color, Comment, Product, Brand


class ListProductCategory(ListView):
    queryset = Product.objects.select_related('category', 'color', 'brand').all()
    template_name = 'store/products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For Filter
        request_get = self.request.GET
        if category := request_get.get('category'):
            context['products'] = context['products'].filter(category__name=category)
        if brand := request_get.get('brand'):
            context['products'] = context['products'].filter(brand__name=brand)
        if color := request_get.get('color'):
            context['products'] = context['products'].filter(color__name=color)

        # Count Of Category & Brand & Color
        context['categories'] = Category.objects.all().annotate(num_product=Count('product'))
        context['brands'] = Brand.objects.all().annotate(num_product=Count('product'))
        context['colors'] = Color.objects.all().annotate(num_product=Count('product'))
        context['values'] = request_get
        return context


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
