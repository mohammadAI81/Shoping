from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db.models import Count
from django.views.generic import ListView, DetailView

from .models import Category, Like, Color, Comment, Product, Brand


class ListProductCategory(ListView):
    paginate_by = 12
    queryset = Product.objects.select_related('category').all()
    template_name = 'store/products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().annotate(num_product=Count('product'))
        context['brands'] = Brand.objects.all().annotate(num_product=Count('product'))
        context['colors'] = Color.objects.all().annotate(num_product=Count('product'))
        return context


class DetailProduct(DetailView):
    queryset = Product.objects.select_related('category', 'brand', 'color')
    template_name = 'store/product.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
