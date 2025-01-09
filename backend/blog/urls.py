from django.urls import path

from .views import BlogView, BlogListView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='index'),
    path('blog/<slug:blog_slug>/', BlogView.as_view(), name='blog-detail'),
]