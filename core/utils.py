import random
import json
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache


def get_random_minute(start_number=30, end_number=60):
    return random.randint(start_number, end_number)


def calculate_order_deliver_at(new_delivery_time):
    return timezone.now() + timedelta(minutes=new_delivery_time)


def calculate_delay_time(deliver_at):
    now = timezone.now()

    if deliver_at > now:
        return 0

    time_diff = now - deliver_at

    mminutes = divmod(time_diff.total_seconds(), 60)

    return mminutes[0]
