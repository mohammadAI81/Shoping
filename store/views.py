from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.db.models import Count, Q
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Comment, Product
from .forms import CommentForm


def list_product_category(request):
    # products = Product.objects.select_related('category', 'color', 'brand')
    #
    # context = {'products': products}

    # # Pagination
    # page_num = request_get.get('page')
    # if context['num'] is None:
    #     context['num'] = request_get.get('num')
    # if page_num or context['num']:
    #     if context['num'] != 'All':
    #         paginator = Paginator(products, context['num'])
    #         products = paginator.get_page(page_num)
    #         context['page_obj'] = products

    # context['products'] = products

    return render(request, 'store/products.html')


class DetailProduct(LoginRequiredMixin, DetailView):
    queryset = Product.objects.select_related('category', 'brand', 'color')
    template_name = 'store/product.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        likes = context['likes'] = context['product'].likes.select_related('person', 'product')
        context['num_likes'] = likes.count()
        context['is_like'] = likes.filter(product=self.get_object(), person=self.request.user).exists()
        context['ratings'] = Comment.RATING_CHOICES
        
        # Start Comments
        comments = context['comments'] = context['product'].comments.filter(published=True)
        context['number1'], context['number2'], context['number3'], context['number4'], context['number5'] = [0,
                                                                                                              0, 0,
                                                                                                              0, 0]

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

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        post = request.POST
        form = CommentForm({'author': user, 'email': user.email, 'product': product, 'published': post.get('published'),
                           'rating': post.get('rating'), 'body': post.get('body')})
        if form.is_valid():
            form.save()
            return redirect('store:product', product.slug)
        else:
            return HttpResponseBadRequest()

        