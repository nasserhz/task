from rest_framework import serializers


from .models import Order, Vendor, Trip, DelayReport


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            "id",
            "status",
        ]


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "id",
            "name",
        ]


class OrderSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(many=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "vendor",
            "created_at",
            "delivery_time",
            "deliver_at",
        ]


class DelayReportSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(many=False)

    class Meta:
        model = DelayReport
        fields = [
            "id",
            "delay",
            "vendor",
        ]
