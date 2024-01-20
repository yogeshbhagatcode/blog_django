from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Blog, Category, Comment


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
    if request.method == 'POST':
        comment = Comment()
        comment.comment = request.POST['comment']
        comment.user = request.user
        comment.blog = blog
        comment.save()
        return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(blog=blog)
    comment_count = comments.count()
    context = {
        'blog' : blog,
        'comments' : comments,
        'comment_count' : comment_count,
    }
    return render(request, 'single_blog.html', context)