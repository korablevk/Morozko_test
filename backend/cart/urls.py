from django.urls import path
from .views import CartView, CartAddView, CartDeleteView, CartUpdateView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='index'),
    path('cart_add/', CartAddView.as_view(), name='cart_add'),
    path('cart_update/', CartUpdateView.as_view(), name='cart_update'),
    path('cart_delete/', CartDeleteView.as_view(), name='cart_delete'),
]