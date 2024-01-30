from django.db import models
from django.utils import timezone
from .utils import calculate_order_deliver_at


class Vendor(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام فروشنده")

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, verbose_name="فروشنده"
    )
    delivery_time = models.PositiveIntegerField(verbose_name="مدت زمان تحویل")
    deliver_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان رسیدن سفارش"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان سفارش"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="زمان ویرایش"
    )

    def __str__(self):
        return f"{self.pk}"

    def is_order_delayed(self) -> bool:
        if self.deliver_at < timezone.now():
            return True
        return False

    def calc_order_delivery_time(self, new_estimate):
        self.delivery_time = new_estimate
        self.deliver_at = calculate_order_deliver_at(
            new_estimate
        )
        return self.save()


class Trip(models.Model):
    TRIP_STATUS_ASSIGNED = "A"
    TRIP_STATUS_AT_VENDOR = "V"
    TRIP_STATUS_PICKED = "P"
    TRIP_STATUS_DELIVERED = "D"

    TRIP_STATUS_CHOICES = [
        (TRIP_STATUS_ASSIGNED, "ASSIGNED"),
        (TRIP_STATUS_AT_VENDOR, "AT VENDOR"),
        (TRIP_STATUS_PICKED, "PICKED"),
        (TRIP_STATUS_DELIVERED, "DELIVERED"),
    ]

    DELIVERY_TIME_CALCULATION_STATUSES = [
        TRIP_STATUS_ASSIGNED,
        TRIP_STATUS_AT_VENDOR,
        TRIP_STATUS_PICKED
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="سفارش",
        related_name="trip"
    )
    status = models.CharField(
        max_length=2,
        choices=TRIP_STATUS_CHOICES,
        null=True,
        verbose_name="وضعیت",
    )
    created_time = models.DateTimeField(
        auto_now=True, verbose_name="زمان ایجاد"
    )

    def __str__(self):
        return f"{self.pk}"

    def is_time_estimation_needed(self) -> bool:
        if self.status in self.DELIVERY_TIME_CALCULATION_STATUSES:
            return True
        return False

    def can_add_to_delay_queue(self):
        if self.status not in self.DELIVERY_TIME_CALCULATION_STATUSES:
            return True
        return False


class DelayReport(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="سفارش"
    )
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, verbose_name="فروشگاه"
    )
    delivery_time = models.PositiveIntegerField(verbose_name="مدت زمان تحویل")
    deliver_at = models.DateTimeField(verbose_name="زمان رسیدن سفارش")
    delay = models.PositiveIntegerField(
        verbose_name="زمان تاخیر",
        null=True,
    )
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان گزارش"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="زمان ویرایش"
    )

    def __str__(self):
        return f"{self.pk}"
