from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
import plotly.graph_objs as go
from django.db.models import Count
from logging_app.models import AccessLog, ErrorLog
from .models import AggregatedAccessLog, AggregatedErrorLog, AggregatedResponseLog
from django.db.models import Count
import pandas as pd
import numpy as np


class GraphsView(View):

    def get(self, request):

        # Recupera i dati per errori e accessi
        errors_by_hour = AggregatedErrorLog.objects.using('gold').values('hour').annotate(count=Count('id'))
        errors_by_day = AggregatedErrorLog.objects.using('gold').values('day').annotate(count=Count('id'))
        access_by_hour = AggregatedAccessLog.objects.using('gold').values('hour').annotate(count=Count('id'))
        access_by_day = AggregatedAccessLog.objects.using('gold').values('day').annotate(count=Count('id'))

        # Grafici
        error_hourly_chart = self.create_hourly_distribution_chart(errors_by_hour, 'Errors by Hour')
        error_daily_chart = self.create_weekly_distribution_chart(errors_by_day, 'Errors by Day of Week')
        access_hourly_chart = self.create_hourly_distribution_chart(access_by_hour, 'Accesses by Hour')
        access_daily_chart = self.create_weekly_distribution_chart(access_by_day, 'Accesses by Day of Week')

        response_codes = AggregatedResponseLog.objects.using('gold').values('response_code').annotate(count=Count('id'))
        response_code_pie_chart = self.create_response_code_pie_chart(response_codes)

        # Passa i dati al template della dashboard
        return render(request, 'gold_bi/graphs.html', {
            'error_hourly_chart': error_hourly_chart,
            'error_daily_chart': error_daily_chart,
            'access_hourly_chart': access_hourly_chart,
            'access_daily_chart': access_daily_chart,
            'response_code_pie_chart': response_code_pie_chart,
        })


    def create_response_code_pie_chart(self, response_codes):
        """
        Crea un grafico a torta che visualizza la distribuzione dei codici di stato delle risposte.
        """
        fig = go.Figure(data=[go.Pie(labels=[entry['response_code'] for entry in response_codes], values=[entry['count'] for entry in response_codes])])
        fig.update_layout(title='Response Code Distribution')
        return fig.to_html(full_html=False)

    def create_weekly_distribution_chart(self, data, title):
        """
        Crea un grafico a barre che mostra il conteggio degli eventi per ogni giorno della settimana.
        """
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[entry['day'] for entry in data], y=[entry['count'] for entry in data]))
        fig.update_layout(title=title, xaxis_title='Day of Week', yaxis_title='Count')
        return fig.to_html(full_html=False)

    def create_hourly_distribution_chart(self, data, title):
        """
        Crea un grafico a barre che mostra il conteggio degli eventi per ogni ora della giornata.
        """
        fig = go.Figure()
        fig.add_trace(go.Bar(x=[entry['hour'] for entry in data], y=[entry['count'] for entry in data]))
        fig.update_layout(title=title, xaxis_title='Hour of Day', yaxis_title='Count')
        return fig.to_html(full_html=False)







class AEListView(View):
    def get(self, request):
        # Recupera i log aggregati per la lista
        accesslogs = AccessLog.objects.order_by('-timestamp')[:50]
        errorlogs = ErrorLog.objects.order_by('-timestamp')[:50]

        # Passa i dati al template della dashboard
        return render(request, 'gold_bi/AElist.html', {
            'accesslogs': accesslogs,
            'errorlogs': errorlogs,
        })


class AccessLogDetailView(View):
    def get(self, request, log_id):
        # Recupera il log specifico
        log = get_object_or_404(AccessLog, pk=log_id)

        # Passa il log al template dei dettagli del log
        return render(request, 'gold_bi/log_detail.html', {'log': log})


class ErrorLogDetailView(View):
    def get(self, request, log_id):
        # Recupera il log specifico
        log = get_object_or_404(ErrorLog, pk=log_id)

        # Passa il log al template dei dettagli del log
        return render(request, 'gold_bi/log_detail.html', {'log': log})

