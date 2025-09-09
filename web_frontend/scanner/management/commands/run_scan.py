"""
Management command para executar scans via Django
"""
import json
import sys
from django.core.management.base import BaseCommand
from django.utils import timezone
from scanner.models import ScanJob, ScanResult
from scanner.serializers import ScanJobSerializer
import os
import django

# Adiciona o diretório pai ao path para importar o port_scanner
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from port_scanner import PortScanner, ScanResult as PortScanResult


class Command(BaseCommand):
    help = 'Executa varredura de portas'

    def add_arguments(self, parser):
        parser.add_argument('--target', type=str, required=True, help='Target para escanear')
        parser.add_argument('--ports', type=str, default='common', help='Portas para escanear')
        parser.add_argument('--protocols', nargs='+', default=['tcp'], help='Protocolos (tcp, udp)')
        parser.add_argument('--timeout', type=int, default=3, help='Timeout em segundos')
        parser.add_argument('--threads', type=int, default=50, help='Número de threads')
        parser.add_argument('--job-id', type=int, help='ID do job no banco de dados')

    def handle(self, *args, **options):
        try:
            # Obter ou criar job no banco
            if options.get('job_id'):
                job = ScanJob.objects.get(id=options['job_id'])
                self.stdout.write(f"Executando job existente: {job.id}")
            else:
                job = ScanJob.objects.create(
                    target=options['target'],
                    ports=options['ports'],
                    protocols=options['protocols'],
                    timeout=options['timeout'],
                    threads=options['threads'],
                    status='running'
                )
                self.stdout.write(f"Criado novo job: {job.id}")

            # Atualizar status para running
            job.status = 'running'
            job.started_at = timezone.now()
            job.save()

            # Executar scan
            scanner = PortScanner()
            
            self.stdout.write(f"Iniciando scan: target={options['target']}, ports={options['ports']}")
            
            results = scanner.scan(
                target=options['target'],
                ports=options['ports'],
                protocols=options['protocols'],
                timeout=options['timeout'],
                threads=options['threads']
            )

            self.stdout.write(f"Scan completado. {len(results)} hosts encontrados.")

            # Salvar resultados no banco
            for result in results:
                scan_result = ScanResult.objects.create(
                    job=job,
                    host=result.host,
                    hostname=result.hostname or '',
                    port=result.port,
                    protocol=result.protocol,
                    status=result.status,
                    service=result.service or '',
                    version=result.version or '',
                    banner=result.banner or ''
                )
                self.stdout.write(f"Salvo resultado: {result.host}:{result.port}/{result.protocol} - {result.status}")

            # Atualizar job como concluído
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.save()

            self.stdout.write(
                self.style.SUCCESS(f'Scan concluído com sucesso! Job ID: {job.id}')
            )

        except ScanJob.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Job {options["job_id"]} não encontrado')
            )
            sys.exit(1)
        except Exception as e:
            # Marcar job como falho se existir
            if 'job' in locals():
                job.status = 'failed'
                job.error_message = str(e)
                job.completed_at = timezone.now()
                job.save()
            
            self.stdout.write(
                self.style.ERROR(f'Erro durante o scan: {e}')
            )
            sys.exit(1)
