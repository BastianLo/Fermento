from django.apps import AppConfig


class BatchesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'batches'


    def ready(self):
        from .scheduler import scheduler
        scheduler.start()
