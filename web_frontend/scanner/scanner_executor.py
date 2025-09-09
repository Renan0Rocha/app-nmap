import sys
import os
import threading
import time
import json
from datetime import datetime
from django.utils import timezone

# Adiciona o diretório pai ao path para importar o port_scanner
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from port_scanner import PortScanner, expand_cidr, expand_port_range, get_common_ports
except ImportError:
    # Fallback se não conseguir importar
    print("Aviso: Não foi possível importar port_scanner. Usando implementação mock.")
    
    class PortScanner:
        def __init__(self, timeout=3, max_threads=50):
            self.timeout = timeout
            self.max_threads = max_threads
            self.results = []
        
        def scan_range(self, hosts, ports, protocols):
            # Mock implementation para desenvolvimento
            time.sleep(2)
            return []
    
    def expand_cidr(cidr):
        return [cidr]
    
    def expand_port_range(ports):
        return [80, 443]
    
    def get_common_ports():
        return {'tcp_common': [80, 443, 22]}

from .models import ScanJob, ScanResult, ScanHistory


class ScanExecutor:
    """Classe responsável por executar varreduras de porta"""
    
    def __init__(self, job_id):
        self.job_id = job_id
        self.job = None
        self.should_stop = False
        
    def execute(self):
        """Executa a varredura"""
        try:
            self.job = ScanJob.objects.get(id=self.job_id)
            self.job.status = 'running'
            self.job.started_at = timezone.now()
            self.job.save()
            
            # Processa parâmetros
            targets = self._process_targets()
            ports = self._process_ports()
            protocols = self._process_protocols()
            
            # Calcula total de verificações
            total_checks = len(targets) * len(ports) * len(protocols)
            self.job.total_ports = total_checks
            self.job.save()
            
            # Executa varredura
            scanner = PortScanner(
                timeout=self.job.timeout,
                max_threads=self.job.threads
            )
            
            # Hook para progresso
            original_scan_host_port = scanner.scan_host_port
            scanned_count = [0]  # Use list para closure
            
            def scan_with_progress(*args, **kwargs):
                if self.should_stop:
                    return
                
                result = original_scan_host_port(*args, **kwargs)
                scanned_count[0] += 1
                
                # Atualiza progresso a cada 10 scans
                if scanned_count[0] % 10 == 0 or scanned_count[0] >= total_checks:
                    progress = min(100, int((scanned_count[0] / total_checks) * 100))
                    ScanJob.objects.filter(id=self.job_id).update(
                        progress=progress,
                        scanned_ports=scanned_count[0]
                    )
                
                return result
            
            scanner.scan_host_port = scan_with_progress
            
            # Executa varredura
            start_time = time.time()
            results = scanner.scan_range(targets, ports, protocols)
            execution_time = time.time() - start_time
            
            if not self.should_stop:
                # Salva resultados
                self._save_results(results)
                
                # Cria histórico
                self._create_history(results, execution_time)
                
                # Atualiza job
                self.job.status = 'completed'
                self.job.completed_at = timezone.now()
                self.job.progress = 100
                self.job.save()
            
        except Exception as e:
            # Em caso de erro
            if self.job:
                self.job.status = 'failed'
                self.job.error_message = str(e)
                self.job.completed_at = timezone.now()
                self.job.save()
            print(f"Erro na varredura: {e}")
    
    def _process_targets(self):
        """Processa string de targets"""
        return expand_cidr(self.job.target)
    
    def _process_ports(self):
        """Processa string de portas"""
        ports_str = self.job.ports.strip()
        
        if ports_str.lower() == 'common':
            common = get_common_ports()
            return common.get('tcp_common', [80, 443])
        elif ports_str.lower() == 'top100':
            return list(range(1, 101))
        elif ports_str.lower() == 'top1000':
            return list(range(1, 1001))
        else:
            return expand_port_range(ports_str)
    
    def _process_protocols(self):
        """Processa protocolos"""
        protocols = []
        if 'TCP' in self.job.protocols.upper():
            protocols.append('TCP')
        if 'UDP' in self.job.protocols.upper():
            protocols.append('UDP')
        return protocols or ['TCP']
    
    def _save_results(self, results):
        """Salva resultados no banco"""
        batch_size = 100
        scan_results = []
        
        for result in results:
            scan_results.append(ScanResult(
                job=self.job,
                host=result.host,
                port=result.port,
                protocol=result.protocol,
                status=result.status,
            ))
            
            # Salva em batches para performance
            if len(scan_results) >= batch_size:
                ScanResult.objects.bulk_create(scan_results, ignore_conflicts=True)
                scan_results = []
        
        # Salva batch final
        if scan_results:
            ScanResult.objects.bulk_create(scan_results, ignore_conflicts=True)
    
    def _create_history(self, results, execution_time):
        """Cria registro de histórico"""
        # Conta resultados por status
        status_counts = {}
        hosts_with_open_ports = set()
        
        for result in results:
            status = result.status
            status_counts[status] = status_counts.get(status, 0) + 1
            
            if status == 'open':
                hosts_with_open_ports.add(result.host)
        
        # Cria resumo
        summary = {
            'target': self.job.target,
            'ports_scanned': self.job.ports,
            'protocols': self.job.protocols,
            'execution_settings': {
                'timeout': self.job.timeout,
                'threads': self.job.threads,
            },
            'results_by_status': status_counts,
            'execution_time': execution_time,
        }
        
        # Salva histórico
        ScanHistory.objects.create(
            job=self.job,
            summary=summary,
            execution_time=execution_time,
            open_ports=status_counts.get('open', 0),
            closed_ports=status_counts.get('closed', 0),
            filtered_ports=status_counts.get('filtered', 0),
            hosts_scanned=len(expand_cidr(self.job.target)),
            hosts_active=len(hosts_with_open_ports),
        )
    
    def stop(self):
        """Para a varredura"""
        self.should_stop = True
        if self.job:
            self.job.status = 'cancelled'
            self.job.completed_at = timezone.now()
            self.job.save()


# Dicionário global para controlar threads de varredura
running_scans = {}


def start_scan(job_id):
    """Inicia uma varredura em thread separada"""
    if job_id in running_scans:
        return False  # Já está executando
    
    executor = ScanExecutor(job_id)
    thread = threading.Thread(target=executor.execute, daemon=True)
    
    running_scans[job_id] = {
        'executor': executor,
        'thread': thread,
        'started_at': datetime.now()
    }
    
    thread.start()
    return True


def stop_scan(job_id):
    """Para uma varredura"""
    if job_id in running_scans:
        running_scans[job_id]['executor'].stop()
        del running_scans[job_id]
        return True
    return False


def get_scan_status(job_id):
    """Obtém status da varredura"""
    return job_id in running_scans
