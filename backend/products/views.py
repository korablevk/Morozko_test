from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from .models import Category, ProductProxy


class ProductListView(ListView):
    model = ProductProxy
    context_object_name = "products"
    paginate_by = 4
    slug_url_kwarg = "category_slug"

    def get_template_names(self):
        return "products/catalog.html"
    
    def get_queryset(self):
        products = super().get_queryset()
        category_slug = self.kwargs.get(self.slug_url_kwarg)

        if category_slug and category_slug != "all":
            products = products.filter(category__slug=category_slug)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()  
        return context


class ProductView(DetailView):
    model = ProductProxy
    template_name = "products/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context