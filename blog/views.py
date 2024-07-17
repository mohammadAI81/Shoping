from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib import messages

from .form import CommentForm
from .models import Comment, Blog


def blogs(request):
    blogs = Blog.objects.annotate(count_comment=Count('comments'))

    context = {
        'blogs': blogs,
    }
    
    return render(request, 'blog/blogs.html', context)


def detail_blog(request, slug):
    blog = get_object_or_404(Blog.objects.prefetch_related('comments'), slug=slug)
    comments = blog.comments.all()
    context = {
        'blog': blog,
        'comments': comments,
        }
    return render(request, 'blog/blog.html', context)
