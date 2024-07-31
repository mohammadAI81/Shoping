from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import Comment, Blog, Reply


class CommentOfBlog(admin.TabularInline):
    model = Comment
    extra = 1
    
    
class ReplyOfComment(admin.TabularInline):
    model = Reply
    extra = 1
    

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'num_comment')
    list_editable = ('published', )
    list_filter = ('published', )
    ordering = ('id', )
    search_fields = ('title', )
    list_per_page = 25
    inlines = [
        CommentOfBlog,
    ]
    readonly_fields = ('slug', )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('comments').annotate(num_comment=Count('comments'))
    
    @admin.display(ordering='num_comment', description='# Comments')
    def num_comment(self, blog):
        return blog.num_comment
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'blog')
    list_per_page = 25
    ordering = ('id', )
    search_fields = ('author',)
    autocomplete_fields = ('blog', )
    list_select_related = ('blog', )
    inlines = [ReplyOfComment]


@admin.register(Reply)
class Reply(admin.ModelAdmin):
    list_display = ('author', 'comment')
    ordering = ('datetime_created', )
    list_per_page = 25
    autocomplete_fields = ('comment',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('comment__blog')
    
    