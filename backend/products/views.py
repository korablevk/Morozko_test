from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .models import Category, ProductProxy


# def products_view(request):
#     products = ProductProxy.objects.all()
#     return render(request, 'shop/catalog.html', {'products': products})

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
        context["categories"] = Category.objects.all()  # Для отображения категорий в шаблоне
        return context



# def products_detail_view(request, slug):
#     product = get_object_or_404(
#         ProductProxy.objects.select_related('category'), slug=slug)

#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             if product.reviews.filter(created_by=request.user).exists():
#                 messages.error(
#                     request, 'You have already made a review for this product.')
#             else:
#                 rating = request.POST.get('rating', 3)
#                 content = request.POST.get('content', '')
#                 if content:
#                     product.reviews.create(
#                         rating=rating, content=content, created_by=request.user, product=product)
#                     return redirect(request.path)
#         else:
#             messages.error(
#                 request, 'You need to be logged in to make a review.')

#     context = {'product': product}
#     return render(request, 'shop/product_detail.html', context)

# def category_list(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     products = ProductProxy.objects.select_related('category').filter(category=category)
#     context = {'category': category, 'products': products}
#     return render(request, 'shop/category_list.html', context)

# def search_products(request):
#     query = request.GET.get('q')
#     products = ProductProxy.objects.filter(title__icontains=query).distinct()
#     context = {'products': products}
#     if not query or not products:
#         return redirect('shop:products')
#     return render(request, 'shop/products.html', context)