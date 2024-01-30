import logging
from celery import shared_task
from .models import Order, DelayReport
from .utils import calculate_delay_time

logger = logging.getLogger('django')


@shared_task(bind=True)
def create_delay_report(self, order_id, vendor_id, delivery_time, deliver_at):
    try:
        order = Order.objects.get(pk=order_id)

        DelayReport.objects.create(
            order=order,
            vendor_id=vendor_id,
            delivery_time=delivery_time,
            deliver_at=deliver_at,
            delay=calculate_delay_time(deliver_at),
        )

        logger.info(
            f"Delay report created for order: {order.pk}"
        )

    except Exception as e:
        logger.error(
            f"create_delay_report had Exception for order id {order_id}"
        )
        raise self.retry(exc=e, countdown=5)
