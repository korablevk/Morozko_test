from datetime import timezone
from django.db import models
from products.models import Product

from accounts.models import User


# class Coupon(models.Model):
#     code = models.CharField(max_length=50, unique=True, verbose_name="Код купона")
#     discount = models.IntegerField(default=1, verbose_name="Скидка (%)")
#     active = models.BooleanField(default=True, verbose_name="Активен")
#     valid_from = models.DateTimeField(null=True, blank=True, verbose_name="Начало действия")
#     valid_to = models.DateTimeField(null=True, blank=True, verbose_name="Конец действия")

#     def is_valid(self):
#         now = timezone.now()
#         return self.active and (self.valid_from is None or self.valid_from <= now) and (self.valid_to is None or self.valid_to >= now)

#     def __str__(self):
#         return f"{self.code} - {self.discount}%"
    
class OrderitemQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    requires_delivery = models.BooleanField(default=False, verbose_name="Требуется доставка")
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(max_length=50, default='В обработке', verbose_name="Статус заказа")
    # coupon = models.ForeignKey(to=Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Купон")
    # discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Сумма скидки")


    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id",)

    # def apply_coupon(self, coupon: Coupon):
        # if coupon.is_valid():
        #     self.coupon = coupon
        #     total_price = self.orderitem_set.aggregate(total=models.Sum(models.F('price') * models.F('quantity')))['total']
        #     self.discount_amount = (total_price * coupon.discount / 100).quantize(Decimal('0.01'))
        # else:
        #     raise ValidationError("Купон недействителен.")

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт", default=None)
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")


    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"
        ordering = ("id",)

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return round(self.product.get_discounted_price() * self.quantity, 2)

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"
    

