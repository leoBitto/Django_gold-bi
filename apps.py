from django.apps import AppConfig

class GoldBiConfig(AppConfig):
    name = 'gold_bi'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from .tasks_scheduler import schedule_tasks
        schedule_tasks()
