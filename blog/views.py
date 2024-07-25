from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator

from .form import CommentForm
from .models import Comment, Blog


def blogs(request):
    blogs = Blog.objects.annotate(count_comments=Count('comments'))
    
    page_num = request.GET.get('page')
    paginator = Paginator(blogs, 5)
    page_obj = paginator.get_page(page_num)
    blogs = page_obj.object_list
    
    # page_obj
    
    context = {
        'blogs': blogs,
        'page_obj': page_obj,
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
            messages.success(request, 'Your comment is submit.')
            print('good')
        else:
            messages.error(request, 'Your comment is not submit')
    
    
    context = {
        'blog': blog,
        'comments': comments,
        'num_comment': count_comment,
        'form': form,
        }
    return render(request, 'blog/blog.html', context)
