from django.contrib import admin
from .models import BlogPost, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'category', 'created_at', 'published_at']
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'body', 'author__username']
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at', 'published_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'body', 'author', 'status')
        }),
        ('分類', {
            'fields': ('category', 'tags')
        }),
        ('日時情報', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
