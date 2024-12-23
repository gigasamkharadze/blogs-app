from django.contrib import admin
from .models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order')
    search_fields = ('title', 'url')
    ordering = ('order',)
