from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .models import Order, Trip, DelayReport
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404
from .tasks import create_delay_report
from delay_report.redis import AgentHash, OrderHash, OrderQueue
from .utils import get_random_minute
import json
from datetime import timedelta
from django.utils import timezone
import logging
from django.db.models import Sum


logger = logging.getLogger('django')


class AddDelayReport(APIView):
    order_queue = OrderQueue()

    def post(self, request: Request):
        order_id = int(request.GET.get('order_id'))

        order = get_object_or_404(Order, pk=order_id)
        trip = Trip.objects.get(order=order)

        if not order.is_order_delayed():
            logger.info(f"Delay request for order {order.pk} rejected.")
            return Response({
                'message': 'Order still has time!',
                'data': OrderSerializer(order).data
            })

        create_delay_report.delay(
            order.pk,
            order.vendor.pk,
            order.delivery_time,
            order.deliver_at,
        )

        order_hash = OrderHash(order.pk)

        if trip.is_time_estimation_needed():
            new_estimate = get_random_minute(start_number=10, end_number=30)
            order.calc_order_delivery_time(new_estimate)
            logger.info(f"Order {order.pk} time estimation done.")

            return Response({
                'message': 'Order new time estimation updated!',
            })

        if trip.can_add_to_delay_queue() and order_hash.add_check():
            self.order_queue.push(OrderSerializer(order).data)
            order_hash.set_defaults()
            logger.info(f"Order {order.pk} added to delay queue.")

            return Response({
                'message': 'Order has been sent to support!',
            })

        return Response({
            'message': 'Order is in support queue!',
        })


class AssignAgent(APIView):
    order_queue = OrderQueue()

    def get(self, request: Request):
        agent_id = int(request.GET.get('agent_id'))

        if self.order_queue.is_empty():
            return Response({
                "message": "سفارشی در صف تاخیر وجود ندارد",
                "data": {},
            })

        agent_hash = AgentHash(agent_id)

        if agent_hash.has_order():
            return Response({
                'message': 'You already has a order to review!',
            })

        item = self.order_queue.pop()
        order = json.loads(item)
        order_hash = OrderHash(order['id'])

        order_hash.set_agent(agent_id)
        agent_hash.set_order(order['id'])

        return Response({
            'message': f"Order {order['id']} assigned to you agent {agent_id}",
        })


class VendorReports(APIView):
    def get(self, request: Request):
        queryset = (
            DelayReport.objects.select_related("vendor")
            .values_list("vendor", "vendor__name")
            .filter(created_time__gte=timezone.now().today()-timedelta(days=7))
            .annotate(delay_sum=Sum('delay'))
            .order_by('-delay_sum')
        )

        result = [
            {
                "id": item[0],
                "vendor": item[1],
                "delay": item[2]
            }
            for item in queryset
        ]

        return Response(result)
