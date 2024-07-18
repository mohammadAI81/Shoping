from django.shortcuts import render, get_object_or_404
from django.db.models import Count, F, Expression
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
    blog = get_object_or_404(Blog, slug=slug)
    comments = blog.comments.all()
    count_comment = len(comments)
    form = CommentForm()
    
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            print('good')
    
    
    context = {
        'blog': blog,
        'comments': comments,
        'num_comment': count_comment,
        'form': form,
        }
    return render(request, 'blog/blog.html', context)
