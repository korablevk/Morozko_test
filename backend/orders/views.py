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


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('accounts:login')

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
                payment_type = self.request.POST.get('payment_type')
                total_price = cart_items.total_price()

                if not cart_items.exists():
                    return JsonResponse({'status': 'error', 'message': 'Корзина пуста.'}, status=400)


                order = Order.objects.create(
                    user=user,
                    phone_number=form.cleaned_data['phone_number'],
                    requires_delivery=form.cleaned_data['requires_delivery'],
                    delivery_address=form.cleaned_data['delivery_address'],
                    payment_on_get=(payment_type == "1"),
                    zip_code=form.cleaned_data['zip_code'],
                )

                for cart_item in cart_items:
                    product = cart_item.product
                    name = product.title
                    price = product.get_discounted_price()
                    quantity = cart_item.quantity

                    if product.quantity < quantity:
                        raise ValidationError(f'Недостаточное количество товара "{name}" на складе. '
                                              f'В наличии: {product.quantity} шт.')

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        name=name,
                        price=price,
                        quantity=quantity,
                    )

                    product.quantity -= quantity
                    product.save()


                messages.success(self.request, 'Заказ оформлен! Ожидайте доставку.')
                cart_items.delete()
                return redirect('account:users_cart')


        except ValidationError as e:
            if order:
                order.delete()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Произошла ошибка при оформлении заказа. {e}'}, status=400)

    def form_invalid(self, form):
        print(f"Form validation errors: {form.errors}") 
        messages.error(self.request, 'Заполните все обязательные поля!')
        return redirect('orders:create_order')
