from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.template.loader import render_to_string

from decimal import Decimal

from products.models import ProductProxy
from .cart import Cart


class CartView(View):
    """Displays the cart."""
    def get(self, request):
        cart = Cart(request)
        context = {
            'cart': cart
        }
        return render(request, 'cart/cart-view.html', context)


class CartAddView(View):
    """Handles adding a product to the cart."""
    def post(self, request):
        if request.POST.get('action') == 'post':
            cart = Cart(request)

            product_id = int(request.POST.get('product_id'))
            product_qty = 1  

            product = get_object_or_404(ProductProxy, id=product_id)

            cart.add(product=product, quantity=product_qty)

            cart_qty = cart.__len__()

            return JsonResponse({'qty': cart_qty, 'product': product.title})


class CartDeleteView(View):
    """Handles deleting a product from the cart."""
    def post(self, request):
        if request.POST.get('action') == 'post':
            cart = Cart(request)

            product_id = request.POST.get('product_id')
            if product_id is None:
                return JsonResponse({'error': 'Product ID is missing'}, status=400)

            try:
                product_id = int(product_id)
                cart.delete(product=product_id)

                cart_qty = cart.__len__()
                cart_total = cart.get_total_price()

                return JsonResponse({'qty': cart_qty, 'total': cart_total})

            except ValueError:
                return JsonResponse({'error': 'Invalid product ID'}, status=400)


class CartUpdateView(View):
    def post(self, request, *args, **kwargs):
        cart_id = request.POST.get('cart_id')
        quantity = int(request.POST.get('quantity'))
        

        cart = Cart(request)
        
        cart.update(cart_id, quantity)
        
        updated_item = cart.cart[cart_id]

        return JsonResponse({
            'quantity': updated_item['quantity'],
            'cart_total': str(cart.get_total_price())
        })
    
        