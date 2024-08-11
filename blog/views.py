from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.utils.html import format_html

from .form import CommentForm, ReplyForm
from .models import Blog


def blogs(request):
    blogs = Blog.object_published.annotate(count_comments=Count('comments'))
    
    # Popular Posts
    comments_count = max([blog['count_comments'] for blog in blogs.values('count_comments')]) // 2
    popular_posts = blogs.filter(count_comments__gte=comments_count).order_by('-count_comments')[:4]
    
    # Search
    search = request.GET.get('search')
    if search:
        blogs = blogs.filter(title__icontains=search)
    
    # Paginator
    page_num = request.GET.get('page')
    paginator = Paginator(blogs, 5)
    page_obj = paginator.get_page(page_num)
    blogs = page_obj.object_list

    context = {
        'blogs': blogs,
        'page_obj': page_obj,
        'popular_posts': popular_posts,
    }
    
    return render(request, 'blog/blogs.html', context)


def detail_blog(request, slug):
    blogs = Blog.object_published.annotate(count_comments=Count('comments'))

    # Popular Posts
    comments_count = max([blog['count_comments'] for blog in blogs.values('count_comments')]) // 2
    popular_posts = blogs.filter(count_comments__gte=comments_count).order_by('-count_comments')[:4]
    
    blog = get_object_or_404(blogs, slug=slug)
    comments = blog.comments.all()
    count_comment = len(comments)
    form = CommentForm()
    
    context = {
        'blog': blog,
        'comments': comments,
        'num_comment': count_comment,
        'form': form,
        'popular_posts': popular_posts,
        }
    return render(request, 'blog/blog.html', context)


@require_POST
def create_comment(request, slug):
    form = CommentForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your comment is submit.')
    else:
        messages.error(request, format_html('Your comment is not submit {}'.format(form.errors)))
    return redirect('blog:blog', slug)


@require_POST
def create_reply_comment(request, slug):
    form = ReplyForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your relpy is submit.')
    else:
        messages.error(request, format_html("Your relpy is not submit {}.".format(form.errors)))
    return redirect('blog:blog', slug)