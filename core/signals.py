
from .models import Trip, Order
from .utils import calculate_order_deliver_at


def order_created_signal(sender, instance, created, **kwargs):
    if created:
        Trip.objects.create(order=instance)

        Order.objects.filter(pk=instance.pk).update(
            deliver_at=calculate_order_deliver_at(
                instance.delivery_time
            )
        )
