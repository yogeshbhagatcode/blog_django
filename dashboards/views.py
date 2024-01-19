from django.shortcuts import render
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def dashboard(request):
    categories_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'blogs_count' : blogs_count,
        'categories_count' : categories_count,
    }
    return render(request, 'dashboard/dashboard.html', context)

def categories(request):
    return render(request, 'dashboard/categories.html')