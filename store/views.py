from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.views.generic import DetailView, CreateView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Like, Color, Comment, Product, Brand
from .variable import SHOW, SORT
from .forms import CommentForm



def list_product_category(request):
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

    context = {'products': products, 'num': request_get.get('page_num')}

    # Pagination
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


class DetailProduct(LoginRequiredMixin, DetailView):
    queryset = Product.objects.select_related('category', 'brand', 'color')
    template_name = 'store/product.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    login_url = reverse_lazy('/account/login/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_like'] = context['product'].likes.count()
        context['ratings'] = Comment.RATING_CHOICES
        context['commetns'] = context['product'].comments.all()
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        post = request.POST
        form = CommentForm({'author': user, 'email': user.email, 'product': product, 'published': post.get('published'),
                           'rating': post.get('rating'), 'body': post.get('body')})
        if form.is_valid():
            form.save()
            return redirect('store:product', product.slug)
    
    