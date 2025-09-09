"""
Django admin configuration for Scanner app
"""
from django.contrib import admin
from .models import ScanJob, ScanResult, ScanHistory


@admin.register(ScanJob)
class ScanJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'target', 'status', 'created_at', 'started_at', 'completed_at')
    list_filter = ('status', 'protocols', 'created_at')
    search_fields = ('target', 'ports')
    readonly_fields = ('created_at', 'started_at', 'completed_at')
    
    fieldsets = (
        ('Configuração do Scan', {
            'fields': ('target', 'ports', 'protocols', 'timeout', 'threads')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'started_at', 'completed_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('job', 'host', 'port', 'protocol', 'status', 'response_time')
    list_filter = ('protocol', 'status', 'job__status')
    search_fields = ('host', 'job__target')
    
    fieldsets = (
        ('Identificação', {
            'fields': ('job', 'host')
        }),
        ('Porta', {
            'fields': ('port', 'protocol', 'status')
        }),
        ('Detalhes', {
            'fields': ('response_time', 'created_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ScanHistory)
class ScanHistoryAdmin(admin.ModelAdmin):
    list_display = ('job', 'hosts_active', 'open_ports', 'execution_time')
    list_filter = ('job__created_at',)
    search_fields = ('job__target', 'summary')
    readonly_fields = ('execution_time',)
    
    fieldsets = (
        ('Scan Info', {
            'fields': ('job', 'hosts_scanned', 'hosts_active', 'execution_time')
        }),
        ('Portas', {
            'fields': ('open_ports', 'closed_ports', 'filtered_ports')
        }),
        ('Resumo', {
            'fields': ('summary',)
        })
    )
