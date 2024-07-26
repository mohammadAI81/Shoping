from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .form import CommentForm
from .models import Comment, Blog


def blogs(request):
    blogs = Blog.objects.annotate(count_comments=Count('comments'))
    
    # Paginator
    page_num = request.GET.get('page')
    paginator = Paginator(blogs, 5)
    page_obj = paginator.get_page(page_num)
    blogs = page_obj.object_list
    
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
    
    
    context = {
        'blog': blog,
        'comments': comments,
        'num_comment': count_comment,
        'form': form,
        }
    return render(request, 'blog/blog.html', context)


@require_POST
def create_comment(request, slug):
    print(request.method)
    form = CommentForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your comment is submit.')
    else:
        messages.error(request, f'Your comment is not submit {form.errors}')
    return redirect('blog:blog', slug)
        
