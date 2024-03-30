from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomAdminPanel(admin.ModelAdmin):
    list_display_links = ('id', 'username')
    list_display = ('id', 'username', 'gender', 'is_staff')
    list_editable = ('gender', )
    ordering = ('username', 'date_joined')
    list_filter = ('is_staff', 'is_superuser')
    list_per_page = 20