from django.db import models
from django.utils import timezone
import uuid


class ScanJob(models.Model):
    """Modelo para armazenar jobs de varredura"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('running', 'Executando'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
        ('cancelled', 'Cancelado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target = models.TextField(help_text="IP, CIDR ou hostname")
    ports = models.TextField(help_text="Lista de portas ou ranges")
    protocols = models.CharField(max_length=10, default='TCP', help_text="TCP, UDP ou ambos")
    timeout = models.IntegerField(default=3, help_text="Timeout em segundos")
    threads = models.IntegerField(default=50, help_text="Número de threads")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    progress = models.IntegerField(default=0, help_text="Progresso em %")
    total_ports = models.IntegerField(default=0)
    scanned_ports = models.IntegerField(default=0)
    
    error_message = models.TextField(blank=True, help_text="Mensagem de erro se falhar")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job de Varredura'
        verbose_name_plural = 'Jobs de Varredura'
    
    def __str__(self):
        return f"Scan {self.target} - {self.status}"


class ScanResult(models.Model):
    """Modelo para armazenar resultados da varredura"""
    
    STATUS_CHOICES = [
        ('open', 'Aberta'),
        ('closed', 'Fechada'),
        ('filtered', 'Filtrada'),
        ('open|filtered', 'Aberta/Filtrada'),
    ]
    
    job = models.ForeignKey(ScanJob, on_delete=models.CASCADE, related_name='results')
    host = models.GenericIPAddressField(help_text="Endereço IP do host")
    port = models.IntegerField(help_text="Número da porta")
    protocol = models.CharField(max_length=5, help_text="TCP ou UDP")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    response_time = models.FloatField(null=True, blank=True, help_text="Tempo de resposta em ms")
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['host', 'port']
        unique_together = ['job', 'host', 'port', 'protocol']
        verbose_name = 'Resultado da Varredura'
        verbose_name_plural = 'Resultados da Varredura'
    
    def __str__(self):
        return f"{self.host}:{self.port}/{self.protocol} - {self.status}"


class ScanHistory(models.Model):
    """Histórico de varreduras para análise"""
    
    job = models.OneToOneField(ScanJob, on_delete=models.CASCADE)
    summary = models.JSONField(help_text="Resumo da varredura em JSON")
    execution_time = models.FloatField(help_text="Tempo total de execução em segundos")
    
    open_ports = models.IntegerField(default=0)
    closed_ports = models.IntegerField(default=0)
    filtered_ports = models.IntegerField(default=0)
    
    hosts_scanned = models.IntegerField(default=0)
    hosts_active = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Histórico de Varredura'
        verbose_name_plural = 'Histórico de Varreduras'
    
    def __str__(self):
        return f"Histórico - {self.job.target}"
