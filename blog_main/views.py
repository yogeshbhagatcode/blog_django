from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from blogs.models import Category, Blog
from side_data.models import OtherInfo
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

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


def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword) , status='Published')
    context = {
        'blogs':blogs,
        'keyword':keyword
    }
    return render(request, 'search.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
            if request.user.has_perm('auth.view_user'):
                return redirect('dashboard')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')