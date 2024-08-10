from django.shortcuts import render
from django.db.models import Count, F


from store.models import Product
from blog.models import Blog


def home(request):
    # Import Data | Blog & Product
    blogs = Blog.object_published.annotate(count_comments=Count('comments'), midcomment=F('count_comments') / 2)
    products = Product.objects.select_related('category').annotate(count_comments=Count('comments'), midcomment=F('count_comments') / 2)
    
    # Popular Blog
    blogs = blogs.filter(count_comments__gte=F('midcomment')).order_by('-count_comments')[:3]

    # Popular Product
    products = products.filter(count_comments__gte=F('midcomment')).order_by('-count_comments')[:7]

    context = {
        'products': products,
        'blogs': blogs,
    }
    return render(request, 'page/home.html', context)


def contact(request):
    return render(request, 'page/contact.html')
