from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import csv
import io

from .models import ScanJob, ScanResult, ScanHistory
from .serializers import (
    ScanJobSerializer, ScanResultSerializer, ScanHistorySerializer,
    ScanJobCreateSerializer, ScanStatusSerializer
)
from .scanner_executor import start_scan, stop_scan, get_scan_status


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão para resultados"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class ScanJobViewSet(viewsets.ModelViewSet):
    """ViewSet para jobs de varredura"""
    
    queryset = ScanJob.objects.all()
    serializer_class = ScanJobSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ScanJobCreateSerializer
        return ScanJobSerializer
    
    def create(self, request):
        """Cria novo job de varredura"""
        serializer = ScanJobCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Processa dados
            data = serializer.validated_data
            
            # Determina portas
            if data.get('use_common_ports'):
                ports = 'common'
            elif data.get('use_top100'):
                ports = 'top100'
            elif data.get('use_top1000'):
                ports = 'top1000'
            else:
                ports = data.get('ports', '80,443')
            
            # Determina protocolos
            protocols = []
            if data.get('tcp'):
                protocols.append('TCP')
            if data.get('udp'):
                protocols.append('UDP')
            
            protocols_str = ','.join(protocols)
            
            # Cria job
            job = ScanJob.objects.create(
                target=data['target'],
                ports=ports,
                protocols=protocols_str,
                timeout=data.get('timeout', 3),
                threads=data.get('threads', 50),
            )
            
            # Inicia varredura
            if start_scan(str(job.id)):
                return Response({
                    'job_id': str(job.id),
                    'message': 'Varredura iniciada com sucesso'
                }, status=status.HTTP_201_CREATED)
            else:
                job.status = 'failed'
                job.error_message = 'Não foi possível iniciar a varredura'
                job.save()
                return Response({
                    'error': 'Falha ao iniciar varredura'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        """Para uma varredura em execução"""
        job = self.get_object()
        
        if job.status != 'running':
            return Response({
                'error': 'Varredura não está em execução'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if stop_scan(str(job.id)):
            return Response({'message': 'Varredura interrompida'})
        else:
            return Response({
                'error': 'Não foi possível interromper a varredura'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def status_detail(self, request, pk=None):
        """Obtém status detalhado da varredura"""
        job = self.get_object()
        
        is_running = get_scan_status(str(job.id))
        
        # Conta resultados
        results_count = job.results.count()
        open_count = job.results.filter(status='open').count()
        closed_count = job.results.filter(status='closed').count()
        filtered_count = job.results.filter(status='filtered').count()
        
        return Response({
            'job_id': str(job.id),
            'status': job.status,
            'progress': job.progress,
            'scanned_ports': job.scanned_ports,
            'total_ports': job.total_ports,
            'is_running': is_running,
            'results_count': results_count,
            'results_summary': {
                'open': open_count,
                'closed': closed_count,
                'filtered': filtered_count,
            },
            'created_at': job.created_at,
            'started_at': job.started_at,
            'completed_at': job.completed_at,
        })
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Obtém resultados da varredura"""
        job = self.get_object()
        
        # Filtros opcionais
        status_filter = request.query_params.get('status')
        host_filter = request.query_params.get('host')
        
        results = job.results.all()
        
        if status_filter:
            results = results.filter(status=status_filter)
        
        if host_filter:
            results = results.filter(host__icontains=host_filter)
        
        # Paginação
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(results, request)
        
        if page is not None:
            serializer = ScanResultSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = ScanResultSerializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def export_csv(self, request, pk=None):
        """Exporta resultados em CSV"""
        job = self.get_object()
        
        # Cria CSV na memória
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Host', 'Port', 'Protocol', 'Status', 'Scanned_At'])
        
        # Dados
        for result in job.results.all():
            writer.writerow([
                result.host,
                result.port,
                result.protocol,
                result.status,
                result.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Prepara resposta
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="scan_results_{job.id}.csv"'
        
        return response


class ScanHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para histórico de varreduras"""
    
    queryset = ScanHistory.objects.all()
    serializer_class = ScanHistorySerializer
    pagination_class = StandardResultsSetPagination


# Views para interface web
def index(request):
    """Página inicial da interface web"""
    return render(request, 'scanner/index_simple.html')


def job_detail(request, job_id):
    """Página de detalhes do job"""
    job = get_object_or_404(ScanJob, id=job_id)
    return render(request, 'scanner/job_detail.html', {'job': job})


@api_view(['GET'])
def scan_statistics(request):
    """Estatísticas gerais das varreduras"""
    total_jobs = ScanJob.objects.count()
    completed_jobs = ScanJob.objects.filter(status='completed').count()
    running_jobs = ScanJob.objects.filter(status='running').count()
    failed_jobs = ScanJob.objects.filter(status='failed').count()
    
    total_results = ScanResult.objects.count()
    open_ports = ScanResult.objects.filter(status='open').count()
    
    return Response({
        'total_jobs': total_jobs,
        'completed_jobs': completed_jobs,
        'running_jobs': running_jobs,
        'failed_jobs': failed_jobs,
        'total_results': total_results,
        'open_ports': open_ports,
        'success_rate': (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0,
    })


@csrf_exempt
@require_http_methods(["POST"])
def quick_scan(request):
    """Endpoint para varredura rápida"""
    try:
        data = json.loads(request.body)
        target = data.get('target', '')
        
        if not target:
            return JsonResponse({'error': 'Target é obrigatório'}, status=400)
        
        # Cria job com configurações padrão
        job = ScanJob.objects.create(
            target=target,
            ports='common',
            protocols='TCP',
            timeout=2,
            threads=100,
        )
        
        # Inicia varredura
        if start_scan(str(job.id)):
            return JsonResponse({
                'job_id': str(job.id),
                'message': 'Varredura rápida iniciada'
            })
        else:
            return JsonResponse({'error': 'Falha ao iniciar varredura'}, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
