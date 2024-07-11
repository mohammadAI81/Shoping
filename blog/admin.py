from django.contrib import admin

from .models import Comment, Blog


class CommentOfBlog(admin.TabularInline):
    model = Comment
    extra = 1
    


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')
    list_editable = ('published', )
    list_filter = ('published', )
    ordering = ('-datetime_created', )
    list_per_page = 10
    fieldsets = (
        (None, {'fields': ('author', 'title', 'description', 'published', 'slug')}),
    )
    inlines = [
        CommentOfBlog,
    ]
    readonly_fields = ('slug', )
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ('author', 'blog')
    list_per_page = 25
    ordering = ('-datetime_created', )
    fieldsets = (
        (None, {'fields': ['blog', 'author', 'description']}),
    )