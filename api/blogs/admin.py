from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Blog, Category, Comment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'is_active')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)
    mptt_level_indent = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'author', 'blog', 'parent', 'created_at')
    list_filter = ('blog', 'author')
    search_fields = ('content',)
    date_hierarchy = 'created_at'