import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delay_report.settings")

celery = Celery("delay_report")
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()
