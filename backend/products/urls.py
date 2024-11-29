from django.urls import path

from .views import ProductListView, ProductView

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='shop'),
    path("<slug:category_slug>/", ProductListView.as_view(), name="category-filter"),
    path('product/<slug:product_slug>/', ProductView.as_view(), name='product-detail'),
]