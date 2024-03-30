from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomAdminPanel(UserAdmin):
    list_display_links = ('id', 'username')
    list_display = ('id', 'username', 'gender', 'is_staff')
    list_editable = ('gender', )
    ordering = ('username', 'date_joined')
    list_filter = ('is_staff', 'is_superuser')
    list_per_page = 20
    model = CustomUser
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ['email']}),
    )
    fieldsets = UserAdmin.fieldsets  + (
        ('Other Fields', {'fields': ['gender', 'birthday', 'stats', 'city']}),
    )