from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.aggregates import Count
from django.utils.html import format_html
from django.core.paginator import Paginator

from .models import Comment, Product, Category, Brand, Color
from .forms import CommentForm
from .variable import SORT


def list_product_category(request):
    queryset_categories = Category.objects.annotate(count_product=Count('products'))
    queryset_brands = Brand.objects.annotate(count_product=Count('products'))
    queryset_colors = Color.objects.annotate(count_product=Count('products'))
    queryset_products = Product.objects.select_related('category').order_by('name').only('name', 'category', 'price', 'slug')
    
    
    
    page = request.GET.get('page')
    paginator = Paginator(queryset_products, 9)
    page_obj = paginator.get_page(number=page)

    context = {
        'categories': queryset_categories,
        'brands': queryset_brands,
        'colors': queryset_colors,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'sorts': SORT,
        
    }
    return render(request, 'store/products.html', context)


class DetailProduct(DetailView):
    queryset = Product.objects.select_related('category', 'brand', 'color').prefetch_related('likes')
    template_name = 'store/product.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        likes = context['likes'] = context['product'].likes.select_related('person', 'product')
        context['ratings'] = Comment.RATING_CHOICES

        # Start Comments
        comments = context['comments'] = context['product'].comments.select_related('author', 'product') \
            .filter(published=True)
        context['number1'], context['number2'], context['number3'], context['number4'], context['number5'] \
            = [0, 0, 0, 0, 0]

        sum_start = 0
        for item in comments:
            if item.rating == '1':
                context['number1'] += 1
            elif item.rating == '2':
                context['number2'] += 1
            elif item.rating == '3':
                context['number3'] += 1
            elif item.rating == '4':
                context['number4'] += 1
            else:
                context['number5'] += 1
            sum_start += int(item.rating)

        if comments.exists():
            context['ave_starts'] = round(sum_start / len(comments), 1)

        return context

    @login_required(login_url='/account/login/')
    def post(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        post = request.POST
        form = CommentForm({'author': user, 'email': user.email, 'product': product, 'published': post.get('published'),
                            'rating': post.get('rating'), 'body': post.get('body')})
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment is success')
            return redirect('store:product', product.slug)
        else:
            messages.error(request, format_html('your comment have Error message. {}'.format(form.errors)))
            return redirect('store:product', product.slug)
