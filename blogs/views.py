from django.shortcuts import get_object_or_404, render
from .models import Blog, Category


def blogs_by_category(request, category_id):
    blogs = Blog.objects.filter(category = category_id, status='Published').order_by('-created_at')
    # category = Category.objects.get(id=category_id)
    category = get_object_or_404(Category, id=category_id)
    context = {
        'blogs':blogs,
        'category':category,
    }
    return render (request, 'blogs_by_category.html', context)


def single_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='Published')
    context = {
        'blog' : blog
    }
    return render(request, 'single_blog.html', context)