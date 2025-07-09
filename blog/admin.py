from django.contrib import admin
from .models import Post, Category, Tag, Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_active', 'published_at')
    search_fields = ('title', 'author__username', 'category__title')
    list_filter = ('is_active', 'published_at', 'created_at')
    ordering = ('-created_at', 'title')

