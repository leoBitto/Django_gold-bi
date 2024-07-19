from django.db import models
from django.utils import timezone

class AggregatedErrorLog(models.Model):
    """
    Modello per memorizzare gli errori aggregati.
    """
    timestamp_aggregation = models.DateTimeField(default=timezone.now)  # Data e ora dell'aggregazione
    hour = models.IntegerField()  # Ora (0-23)
    day = models.CharField(max_length=10)  # Giorno della settimana (es. "Monday")
    count = models.IntegerField()  # Conteggio degli errori

    class Meta:
        verbose_name = "Aggregated Error Log"
        verbose_name_plural = "Aggregated Error Logs"
        ordering = ['timestamp_aggregation']

    def __str__(self):
        return f"Error Log - {self.timestamp_aggregation} - Count: {self.count}"


class AggregatedAccessLog(models.Model):
    """
    Modello per memorizzare gli accessi aggregati.
    """
    timestamp_aggregation = models.DateTimeField(default=timezone.now)  # Data e ora dell'aggregazione
    hour = models.IntegerField()  # Ora (0-23)
    day = models.CharField(max_length=10)  # Giorno della settimana (es. "Monday")
    count = models.IntegerField()  # Conteggio degli accessi

    class Meta:
        verbose_name = "Aggregated Access Log"
        verbose_name_plural = "Aggregated Access Logs"
        ordering = ['timestamp_aggregation']

    def __str__(self):
        return f"Access Log - {self.timestamp_aggregation} - Count: {self.count}"


class AggregatedResponseLog(models.Model):
    """
    Modello per memorizzare i codici di risposta aggregati.
    """
    timestamp_aggregation = models.DateTimeField(default=timezone.now)  # Data e ora dell'aggregazione
    hour = models.IntegerField()  # Ora (0-23)
    day = models.CharField(max_length=10)  # Giorno della settimana (es. "Monday")
    response_code = models.CharField(max_length=3)  # Codice di risposta (es. "200", "404")
    count = models.IntegerField()  # Conteggio dei codici di risposta

    class Meta:
        verbose_name = "Aggregated Response Log"
        verbose_name_plural = "Aggregated Response Logs"
        ordering = ['timestamp_aggregation']

    def __str__(self):
        return f"Response Log - {self.timestamp_aggregation} - Code: {self.response_code} - Count: {self.count}"