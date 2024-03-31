from django.contrib import admin

from .models import Color, Category, Comment, Product, Like, Brand


class CommentProduct(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ('name', )
    list_per_page = 10


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    list_per_page = 10


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 10
    ordering = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'rating', 'published')
    list_editable = ('product', 'published')
    list_filter = ('published', 'rating')
    list_per_page = 25
    ordering = ('datetime_created', )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('person', 'product')
    list_filter = ('person', )
    list_per_page = 50
    ordering = ('person', 'product')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory', 'category', 'price', 'discount', 'availability')
    list_editable = ('inventory', 'price', 'discount')
    list_filter = ('category', 'discount', 'availability')
    list_per_page = 35
    ordering = ('name', 'category')
    inlines = [
        CommentProduct,
    ]

