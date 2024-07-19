from django_q.tasks import schedule
from django.utils import timezone

def schedule_tasks():
    # Schedula l'aggregazione dei log di accesso ogni giorno a mezzanotte
    schedule(
        'gold_bi.tasks.logging.aggregate_access_logs.aggregate_access_logs',
        schedule_type='D',
        repeats=-1,  # Ripeti indefinitamente
        next_run=timezone.now() + timezone.timedelta(days=1)
    )

    # Schedula l'aggregazione dei log di errori ogni giorno a mezzanotte
    schedule(
        'gold_bi.tasks.logging.aggregate_error_logs.aggregate_error_logs',
        schedule_type='D',
        repeats=-1,  # Ripeti indefinitamente
        next_run=timezone.now() + timezone.timedelta(days=1)
    )

    # Schedula l'aggregazione dei codici di risposta ogni giorno a mezzanotte
    schedule(
        'gold_bi.tasks.logging.aggregate_response_logs.aggregate_response_logs',
        schedule_type='D',
        repeats=-1,  # Ripeti indefinitamente
        next_run=timezone.now() + timezone.timedelta(days=1)
    )
