from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Order, OrderItem


@shared_task()
def send_order_confirmation(order_id):
    try:
        order = Order.objects.get(id=order_id)
 
        order_items = OrderItem.objects.filter(order=order)
        item_details = "\n".join(
            [f"{item.name} (x{item.quantity}) - {item.price} руб." for item in order_items]
        )
        total_price = sum(item.products_price() for item in order_items)
        
        subject = f"Подтверждение заказа №{order.id}"
        message = (
            f"Уважаемый {order.user.first_name} {order.user.last_name},\n\n"
            f"Ваш заказ №{order.id} успешно оформлен!\n\n"
            f"Детали заказа:\n"
            f"{item_details}\n\n"
            f"Общая стоимость: {total_price} руб.\n\n"
            f"Доставка: {'Да' if order.requires_delivery else 'Нет'}\n"
            f"Адрес доставки: {order.delivery_address if order.delivery_address else 'Не указан'}\n\n"
            f"Спасибо за ваш заказ!\n"
        )
    

        mail_to_sender = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        

        admin_subject = f"Новый заказ №{order.id}"
        admin_message = (
            f"Новый заказ оформлен.\n\n"
            f"Номер заказа: {order.id}\n"
            f"Имя клиента: {order.user.first_name} {order.user.last_name}\n"
            f"Общая стоимость: {total_price} руб.\n"
        )
        
        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["kzn.morozko@gmail.com"],
            fail_silently=False,
        )
        
        return mail_to_sender

    except Order.DoesNotExist:
        return f"Order with id {order_id} does not exist"
    except Exception as e:
        return f"Error sending email for order {order_id}: {str(e)}"
