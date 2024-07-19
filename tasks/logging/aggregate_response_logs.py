from django.utils import timezone
from logging_app.models import AccessLog
from gold_bi.models import AggregatedResponseLog
from django.db import transaction

def aggregate_response_logs():
    """
    Aggrega i codici di risposta per ora e giorno della settimana.
    """
    now = timezone.now()
    start_time = now - timezone.timedelta(days=1)
    end_time = start_time + timezone.timedelta(days=1)
    
    access_logs = AccessLog.objects.filter(timestamp__gte=start_time, timestamp__lt=end_time)
    
    response_aggregation = access_logs.values('response_code').annotate(count=models.Count('id'))
    
    with transaction.atomic(using='gold'):
        for entry in response_aggregation:
            AggregatedResponseLog.objects.update_or_create(
                timestamp_aggregation=start_time,
                response_code=entry['response_code'],
                defaults={'count': entry['count']}
            ).using('gold')
