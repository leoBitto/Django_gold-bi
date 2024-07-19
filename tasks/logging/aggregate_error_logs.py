from django.utils import timezone, dateparse
from logging_app.models import ErrorLog
from gold_bi.models import AggregatedErrorLog
from django.db import transaction

def aggregate_error_logs():
    """
    Aggrega i log di errore per ora e giorno della settimana.
    """
    now = timezone.now()
    start_time = now - timezone.timedelta(days=1)
    end_time = start_time + timezone.timedelta(days=1)
    
    logs = ErrorLog.objects.filter(timestamp__gte=start_time, timestamp__lt=end_time)
    
    # Aggregazione per ora e giorno della settimana
    aggregation = logs.annotate(
        hour=models.functions.ExtractHour('timestamp'),
        day=models.functions.ExtractWeekDay('timestamp')
    ).values('hour', 'day').annotate(count=models.Count('id'))
    
    with transaction.atomic(using='gold'):
        for entry in aggregation:
            AggregatedErrorLog.objects.update_or_create(
                timestamp_aggregation=start_time,
                hour=entry['hour'],
                day=entry['day'],
                defaults={'count': entry['count']}
            ).using('gold')
