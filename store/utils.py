from django.db import transaction
from .models import Order, OrderItem


def create_order(user):
    cart = user.cart
    if not cart.items.exists():
        return None

    order = Order.objects.create(user=user)

    try:
        with transaction.atomic():
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart.items.all().delete()
            order.save()

    except Exception as e:

        order.save()
        return None

    return order
