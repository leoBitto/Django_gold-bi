from django.utils import timezone
from logging_app.models import ErrorLog  # Assumendo che questo modello esista e sia simile ad AccessLog
from gold_bi.models import AggregatedErrorLog
from django.db.models import Count, F
from django.db.models.functions import ExtractHour, ExtractWeekDay

def aggregate_error_logs():
    """
    Aggrega i log di errore per ora e giorno della settimana.
    """
    now = timezone.now()
    start_time = now - timezone.timedelta(days=1)
    end_time = start_time + timezone.timedelta(days=1)
    
    error_aggregations = ErrorLog.objects.using('default').filter(
        timestamp__gte=start_time, timestamp__lt=end_time
    ).annotate(
        hour=ExtractHour('timestamp'),
        day=ExtractWeekDay('timestamp')
    ).values('hour', 'day').annotate(
        count=Count('id')
    ).values('hour', 'day', 'count')

    
   # Inserimento dei risultati aggregati nel modello AggregatedErrorLog
    for aggregation in error_aggregations:
        AggregatedErrorLog.objects.using('gold').update_or_create(
            timestamp_aggregation=now,
            hour=aggregation['hour'],
            day=aggregation['day'],
            defaults={'count': aggregation['count']}
        )