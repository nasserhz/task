from django.contrib import admin

from .models import (
    Vendor,
    Order,
    Trip,
    DelayReport,
)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    show_full_result_count = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "delivery_time",
        "vendor",
        "created_at",
        "updated_at",
        "deliver_at",
    ]
    show_full_result_count = False


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "order", "created_time"]
    readonly_fields = ["order"]
    show_full_result_count = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(DelayReport)
class DelayReportAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "vendor",
        "delivery_time",
        "deliver_at",
        "delay",
        "created_time"
    ]
    show_full_result_count = False
