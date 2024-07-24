from django.contrib import admin
from gold_bi.models import AggregatedErrorLog, AggregatedAccessLog

@admin.register(AggregatedErrorLog)
class AggregatedErrorLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp_aggregation', 'hour', 'day', 'count')
    list_filter = ('day', 'hour')
    search_fields = ('day',)
    ordering = ('timestamp_aggregation',)

@admin.register(AggregatedAccessLog)
class AggregatedAccessLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp_aggregation', 'hour', 'day', 'count')
    list_filter = ('day', 'hour')
    search_fields = ('day',)
    ordering = ('timestamp_aggregation',)

