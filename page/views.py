from django.shortcuts import render
from django.db.models import Count


from store.models import Product
from blog.models import Blog

def home(request):
    # Import Data | Blog & Product
    blogs = Blog.object_published.annotate(count_comments=Count('comments'))
    products = Product.objects.select_related('category', 'brand', 'color').annotate(count_comments=Count('comments'))
    
    # Popular Blog
    comments_count = max([blog['count_comments'] for blog in blogs.values('count_comments')]) // 2
    blogs = blogs.filter(count_comments__gte=comments_count).order_by('-count_comments')[:3]

    # Popular Product
    product_count_comment = max([product['count_comments'] for product in products.values('count_comments')]) // 2
    products = products.filter(count_comments__gte=product_count_comment).order_by('-count_comments')[:7]
    
    
    context = {
        'products': products,
        'blogs': blogs,
    }
    return render(request, 'page/home.html', context)

def contact(request):
    return render(request, 'page/contact.html')
