from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from blogs.models import Category, Blog
from side_data.models import OtherInfo

def home(request):
    categories = Category.objects.all()
    featured_blogs = Blog.objects.filter(is_featured=True, status='Published').order_by('-created_at')
    recent_blogs = Blog.objects.filter(is_featured=False, status='Published').order_by('-created_at')
    other_info = OtherInfo.objects.all()

    context = {
        'categories' : categories,
        'featured_blogs' : featured_blogs,
        'recent_blogs' : recent_blogs,
        'other_info' : other_info,
    }
    return render(request, 'home.html', context)


def single_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='Published')
    context = {
        'blog' : blog
    }
    return render(request, 'single_blog.html', context)


def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword) , status='Published')
    context = {
        'blogs':blogs,
        'keyword':keyword
    }
    return render(request, 'search.html', context)