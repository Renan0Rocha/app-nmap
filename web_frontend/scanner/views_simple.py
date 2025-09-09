"""
View simples para executar scan básico
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import sys
import os

# Tentar importar port_scanner
try:
    # Primeiro tentar do diretório atual
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from port_scanner import PortScanner, expand_cidr, expand_port_range
    SCANNER_AVAILABLE = True
    print("✓ Port scanner importado com sucesso!")
except ImportError:
    try:
        # Tentar do diretório pai
        parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        sys.path.insert(0, parent_dir)
        from port_scanner import PortScanner, expand_cidr, expand_port_range
        SCANNER_AVAILABLE = True
        print("✓ Port scanner importado com sucesso (caminho alternativo)!")
    except ImportError as e:
        SCANNER_AVAILABLE = False
        print(f"✗ Erro ao importar port_scanner: {e}")
except Exception as e:
    SCANNER_AVAILABLE = False
    print(f"✗ Erro inesperado: {e}")

@csrf_exempt
@require_http_methods(["POST"])
def simple_scan(request):
    """Endpoint para executar scan básico"""
    
    print(f"📡 Requisição recebida: {request.method}")
    print(f"📡 Body da requisição: {request.body}")
    
    if not SCANNER_AVAILABLE:
        print("❌ Scanner não disponível!")
        return JsonResponse({
            'success': False,
            'error': 'Port Scanner não disponível. Execute o scan manualmente via CLI.',
            'cli_command': 'python port_scanner.py -t {target} -p {ports}'
        })
    
    try:
        data = json.loads(request.body)
        target = data.get('target')
        ports = data.get('ports', 'common')
        protocols = data.get('protocols', ['tcp'])
        timeout = int(data.get('timeout', 3))
        threads = int(data.get('threads', 50))
        
        print(f"🎯 Dados parseados:")
        print(f"   Target: {target}")
        print(f"   Portas: {ports}")
        print(f"   Protocolos: {protocols}")
        print(f"   Timeout: {timeout}")
        print(f"   Threads: {threads}")
        
        if not target:
            print("❌ Target não fornecido!")
            return JsonResponse({
                'success': False,
                'error': 'Target é obrigatório'
            })
        
        # Expandir targets e portas
        targets = expand_cidr(target)
        
        # Processar portas
        if ports == 'common':
            port_list = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 8080]
        else:
            port_list = expand_port_range(ports)
        
        # Criar instância do scanner
        scanner = PortScanner(timeout=timeout, max_threads=threads)
        
        # Executar scan
        results = scanner.scan_range(
            hosts=targets,
            ports=port_list,
            protocols=[p.upper() for p in protocols]
        )
        
        # Converter resultados para formato JSON
        scan_results = []
        for result in results:
            scan_results.append({
                'host': result.host,
                'hostname': result.host,  # Usar o IP como hostname por ora
                'port': result.port,
                'protocol': result.protocol.lower(),
                'status': result.status,
                'service': None,  # Não disponível na versão atual
                'version': None,  # Não disponível na versão atual
                'banner': None    # Não disponível na versão atual
            })
        
        return JsonResponse({
            'success': True,
            'results': scan_results,
            'total_results': len(scan_results),
            'open_ports': len([r for r in scan_results if r['status'] == 'open'])
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
