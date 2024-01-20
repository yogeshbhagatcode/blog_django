from django.contrib import admin
from .models import Category, Blog, Comment

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured')
    search_fields = ('title', 'category__category_name', 'author__username', 'status')

admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)