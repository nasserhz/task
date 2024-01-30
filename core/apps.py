from django.apps import AppConfig
from django.db.models.signals import post_save


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from . import signals

        post_save.connect(
            signals.order_created_signal,
            sender=self.get_model('Order'),
            dispatch_uid="order_created_signal",
        )
