from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from cart.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from orders.tasks import send_order_confirmation


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('account:users-cart')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)
                payment_type = form.cleaned_data.get('payment_on_get')
                requires_delivery = form.cleaned_data['requires_delivery'] == "1"
                delivery_address = form.cleaned_data['delivery_address']

                if form.cleaned_data.get('coupon_code'):
                    coupon = form.cleaned_data['coupon_code']
                    order.apply_coupon(coupon)
                    order.save()

                if not cart_items.exists():
                    return JsonResponse({'status': 'error', 'message': 'Корзина пуста!'}, status=400)

                if requires_delivery and not delivery_address:
                    return JsonResponse({'status': 'error', 'message': 'Адрес доставки обязателен, если выбрана доставка.'}, status=400)

                if payment_type is None:
                    return JsonResponse({'status': 'error', 'message': 'Выберите способ оплаты!'}, status=400)

                order = Order.objects.create(
                    user=user,
                    phone_number=form.cleaned_data['phone_number'],
                    requires_delivery=requires_delivery,
                    delivery_address=delivery_address,
                    payment_on_get=(payment_type == "1"),
                    zip_code=form.cleaned_data['zip_code'],
                )

                for cart_item in cart_items:
                    product = cart_item.product
                    name = product.title
                    price = product.get_discounted_price()
                    quantity = cart_item.quantity

                    if product.quantity < quantity:
                        return JsonResponse({'status': 'error', 'message': f'Недостаточное количество товара "{name}" на складе. В наличии: {product.quantity} шт.'}, status=400)
                        #raise ValidationError(f'Недостаточное количество товара "{name}" на складе. В наличии: {product.quantity} шт.')

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        name=name,
                        price=price,
                        quantity=quantity,
                    )

                    product.quantity -= quantity
                    product.save()

                send_order_confirmation.delay(order.id)

                cart_items.delete()

                messages.success(self.request, 'Заказ оформлен!')
                return JsonResponse({'status': 'success', 'message': 'Заказ успешно оформлен.'}, status=200)

        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Произошла ошибка: {str(e)}'}, status=500)

    def form_invalid(self, form):
        print(f"Form validation errors: {form.errors}")
        return JsonResponse({'status': 'error', 'message': 'Заполните все обязательные поля!'}, status=400)
