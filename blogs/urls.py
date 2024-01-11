from django.urls import path
from .import views

urlpatterns = [
    path('<int:category_id>/', views.blogs_by_category, name='blogs_by_category'),
    path('<slug:slug>/', views.single_blog, name='single_blog'),
]