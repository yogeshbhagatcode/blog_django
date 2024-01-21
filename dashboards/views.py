from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CategoryForm, BlogForm
from django.template.defaultfilters import slugify
from .forms import UserAddForm, UserEditForm


def permission_required(permission):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.has_perm(permission):
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home')
        return wrapper
    return decorator


@login_required(login_url='login')
@permission_required('blogs.change_blog')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()

    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


@permission_required('blogs.view_category')
def categories(request):
    return render(request, 'dashboard/categories.html')


@permission_required('blogs.add_category')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    context = {
        'form' : form,
    }
    return render(request, 'dashboard/add_category.html', context)


@permission_required('blogs.change_category')
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form' : form,
        'category' : category,
    }
    return render(request, 'dashboard/edit_category.html', context)


@permission_required('blogs.delete_category')
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')


@permission_required('blogs.view_blog')
def blogs(request):
    blogs = Blog.objects.all()
    context = {
        'blogs' : blogs,
    }
    return render(request, 'dashboard/blogs.html', context)


@permission_required('blogs.add_blog')
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            title = form.cleaned_data['title'] + '-' + str(blog.id)
            blog.slug = slugify(title)
            blog.save()
            return redirect('blogs')
    else:
        form = BlogForm()
    context = {
        'form' : form,
    }
    return render(request, 'dashboard/add_blog.html', context)


@permission_required('blogs.change_blog')
def edit_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save()
            title = form.cleaned_data['title']
            blog.slug = slugify(title) + '-' + str(blog.id)
            blog.save()
            return redirect('blogs')

    else:
        form = BlogForm(instance=blog)
    context = {
        'form' : form,
        'blog' : blog,
    }
    return render(request, 'dashboard/edit_blog.html', context)


@permission_required('blogs.delete_blog')
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect('blogs')


@permission_required('auth.view_user')
def users(request):
    users = User.objects.all()
    context = {
        'users' : users,
    }
    return render(request, 'dashboard/users.html', context)


@permission_required('auth.add_user')
def add_user(request):
    if request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
            
    else:
        form = UserAddForm()
    context = {
        'form' : form
    }
    return render(request, 'dashboard/add_user.html', context)


@permission_required('auth.change_user')
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = UserEditForm(instance=user)
    context = {
        'form' : form,
        'user' : user,
    }
    return render(request, 'dashboard/edit_user.html', context)    


@permission_required('auth.delete_user')
def delete_user(request,pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')