from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from .models import Blogs


class BlogListView(ListView):
    model = Blogs
    context_object_name = "blogs"
    paginate_by = 6

    def get_template_names(self):
        return "blog/blog.html"
    
    def get_queryset(self):
        blogs = super().get_queryset()
        return blogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BlogView(DetailView):
    model = Blogs
    template_name = "blog/blog_page.html"
    slug_url_kwarg = "blog_slug"
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context