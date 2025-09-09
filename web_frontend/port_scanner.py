#!/usr/bin/env python3
"""
Ferramenta de Varredura de Portas TCP e UDP
Desenvolvida para detectar portas abertas, fechadas e filtradas em redes
"""

import socket
import threading
import time
import argparse
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Dict, Set
import sys
import struct


@dataclass
class ScanResult:
    """Classe para armazenar resultado da varredura"""
    host: str
    port: int
    protocol: str
    status: str  # 'open', 'closed', 'filtered'


class PortScanner:
    """Classe principal para varredura de portas"""
    
    def __init__(self, timeout=3, max_threads=100):
        self.timeout = timeout
        self.max_threads = max_threads
        self.results = []
        self.lock = threading.Lock()
        
    def scan_tcp_port(self, host: str, port: int) -> ScanResult:
        """
        Realiza varredura TCP em uma porta específica usando SYN scan básico
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # Tenta conectar na porta
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return ScanResult(host, port, 'TCP', 'open')
            else:
                return ScanResult(host, port, 'TCP', 'closed')
                
        except socket.timeout:
            return ScanResult(host, port, 'TCP', 'filtered')
        except socket.error:
            return ScanResult(host, port, 'TCP', 'filtered')
            
    def scan_udp_port(self, host: str, port: int) -> ScanResult:
        """
        Realiza varredura UDP em uma porta específica
        UDP é mais complexo pois é um protocolo sem conexão
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            
            # Envia um pacote UDP vazio ou com dados genéricos
            message = b"UDP_SCAN_TEST"
            sock.sendto(message, (host, port))
            
            try:
                # Tenta receber uma resposta
                sock.recvfrom(1024)
                sock.close()
                return ScanResult(host, port, 'UDP', 'open')
            except socket.timeout:
                # Timeout pode indicar que a porta está aberta (sem resposta)
                # ou filtrada. Para UDP, assumimos aberta se não há erro ICMP
                sock.close()
                return ScanResult(host, port, 'UDP', 'open|filtered')
            except ConnectionRefusedError:
                # ICMP Port Unreachable - porta fechada
                sock.close()
                return ScanResult(host, port, 'UDP', 'closed')
                
        except socket.error as e:
            return ScanResult(host, port, 'UDP', 'filtered')
            
    def scan_host_port(self, host: str, port: int, protocol: str) -> None:
        """Escaneia uma porta específica de um host"""
        if protocol.upper() == 'TCP':
            result = self.scan_tcp_port(host, port)
        elif protocol.upper() == 'UDP':
            result = self.scan_udp_port(host, port)
        else:
            return
            
        with self.lock:
            self.results.append(result)
            
    def scan_range(self, hosts: List[str], ports: List[int], protocols: List[str] = None) -> List[ScanResult]:
        """
        Escaneia uma lista de hosts em uma lista de portas
        """
        if protocols is None:
            protocols = ['TCP']
            
        print(f"[+] Iniciando varredura de {len(hosts)} host(s) em {len(ports)} porta(s)")
        print(f"[+] Protocolos: {', '.join(protocols)}")
        print(f"[+] Timeout: {self.timeout}s | Max Threads: {self.max_threads}")
        print("-" * 60)
        
        self.results = []
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            
            for host in hosts:
                for port in ports:
                    for protocol in protocols:
                        future = executor.submit(self.scan_host_port, host, port, protocol)
                        futures.append(future)
            
            # Aguarda conclusão de todas as threads
            completed = 0
            total = len(futures)
            
            for future in futures:
                future.result()
                completed += 1
                if completed % 50 == 0 or completed == total:
                    print(f"[+] Progresso: {completed}/{total} ({(completed/total)*100:.1f}%)")
        
        return self.results
        
    def display_results(self) -> None:
        """Exibe os resultados da varredura de forma organizada"""
        if not self.results:
            print("[-] Nenhum resultado encontrado")
            return
            
        # Organiza resultados por status
        open_ports = [r for r in self.results if r.status == 'open']
        open_filtered = [r for r in self.results if 'open' in r.status and 'filtered' in r.status]
        closed_ports = [r for r in self.results if r.status == 'closed']
        filtered_ports = [r for r in self.results if r.status == 'filtered']
        
        print("\n" + "="*60)
        print("RESULTADOS DA VARREDURA")
        print("="*60)
        
        if open_ports:
            print(f"\n[+] PORTAS ABERTAS ({len(open_ports)}):")
            for result in sorted(open_ports, key=lambda x: (x.host, x.port)):
                print(f"    {result.host}:{result.port}/{result.protocol} - {result.status.upper()}")
                
        if open_filtered:
            print(f"\n[?] PORTAS ABERTAS|FILTRADAS ({len(open_filtered)}):")
            for result in sorted(open_filtered, key=lambda x: (x.host, x.port)):
                print(f"    {result.host}:{result.port}/{result.protocol} - {result.status.upper()}")
        
        if closed_ports:
            print(f"\n[-] PORTAS FECHADAS ({len(closed_ports)}):")
            # Mostra apenas algumas para não poluir a saída
            for result in sorted(closed_ports, key=lambda x: (x.host, x.port))[:10]:
                print(f"    {result.host}:{result.port}/{result.protocol} - {result.status.upper()}")
            if len(closed_ports) > 10:
                print(f"    ... e mais {len(closed_ports) - 10} portas fechadas")
                
        if filtered_ports:
            print(f"\n[!] PORTAS FILTRADAS ({len(filtered_ports)}):")
            for result in sorted(filtered_ports, key=lambda x: (x.host, x.port))[:10]:
                print(f"    {result.host}:{result.port}/{result.protocol} - {result.status.upper()}")
            if len(filtered_ports) > 10:
                print(f"    ... e mais {len(filtered_ports) - 10} portas filtradas")
        
        print(f"\n[*] Total de portas escaneadas: {len(self.results)}")
        
    def save_results(self, filename: str) -> None:
        """Salva os resultados em um arquivo"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Host,Port,Protocol,Status\n")
                for result in sorted(self.results, key=lambda x: (x.host, x.port)):
                    f.write(f"{result.host},{result.port},{result.protocol},{result.status}\n")
            print(f"[+] Resultados salvos em: {filename}")
        except Exception as e:
            print(f"[-] Erro ao salvar arquivo: {e}")


def expand_cidr(cidr: str) -> List[str]:
    """Expande notação CIDR para lista de IPs ou processa lista de IPs separados por vírgula"""
    # Se contém vírgula, trata como lista de IPs
    if ',' in cidr:
        ips = []
        for ip_part in cidr.split(','):
            ip_part = ip_part.strip()
            try:
                # Verifica se é CIDR
                if '/' in ip_part:
                    network = ipaddress.ip_network(ip_part, strict=False)
                    ips.extend([str(ip) for ip in network.hosts()])
                else:
                    # Valida IP único
                    ipaddress.ip_address(ip_part)
                    ips.append(ip_part)
            except ValueError:
                # Se não é IP válido, adiciona como hostname
                ips.append(ip_part)
        return ips
    
    # Processa CIDR único ou IP único
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError:
        return [cidr]  # Retorna o IP original se não for CIDR válido


def expand_port_range(port_range: str) -> List[int]:
    """Expande range de portas (ex: 1-1000, 80,443,8080)"""
    ports = []
    
    for part in port_range.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
            
    return sorted(list(set(ports)))


def get_common_ports() -> Dict[str, List[int]]:
    """Retorna listas de portas comuns para diferentes protocolos"""
    return {
        'tcp_common': [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080],
        'udp_common': [53, 67, 68, 69, 123, 161, 162, 514, 1194, 4500],
        'tcp_top100': list(range(1, 101)),
        'tcp_top1000': list(range(1, 1001)),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Ferramenta de Varredura de Portas TCP e UDP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python port_scanner.py -t 192.168.1.1 -p 80,443,8080
  python port_scanner.py -t 192.168.1.0/24 -p 1-1000 --tcp --udp
  python port_scanner.py -t 10.0.0.1 --common-ports
  python port_scanner.py -t example.com -p 80-90 --timeout 5 --threads 50
        """
    )
    
    parser.add_argument('-t', '--target', required=True, 
                       help='IP/CIDR/hostname do destino (ex: 192.168.1.1, 192.168.1.0/24)')
    parser.add_argument('-p', '--ports', 
                       help='Portas para escanear (ex: 80,443 ou 1-1000)')
    parser.add_argument('--tcp', action='store_true', default=False,
                       help='Escanear portas TCP')
    parser.add_argument('--udp', action='store_true', default=False,
                       help='Escanear portas UDP')
    parser.add_argument('--common-ports', action='store_true',
                       help='Escanear portas comuns')
    parser.add_argument('--top100', action='store_true',
                       help='Escanear top 100 portas TCP')
    parser.add_argument('--top1000', action='store_true',
                       help='Escanear top 1000 portas TCP')
    parser.add_argument('--timeout', type=float, default=3,
                       help='Timeout por conexão em segundos (padrão: 3)')
    parser.add_argument('--threads', type=int, default=100,
                       help='Número máximo de threads (padrão: 100)')
    parser.add_argument('-o', '--output',
                       help='Arquivo para salvar resultados (CSV)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Saída detalhada')
    
    args = parser.parse_args()
    
    # Valida argumentos
    if not any([args.ports, args.common_ports, args.top100, args.top1000]):
        print("[-] Erro: Especifique portas para escanear (-p, --common-ports, --top100 ou --top1000)")
        sys.exit(1)
    
    if not args.tcp and not args.udp:
        args.tcp = True  # TCP por padrão
    
    # Expande targets
    print("[+] Expandindo lista de targets...")
    targets = expand_cidr(args.target)
    print(f"[+] Targets encontrados: {len(targets)}")
    
    if args.verbose:
        print(f"[+] Targets: {', '.join(targets[:10])}")
        if len(targets) > 10:
            print(f"    ... e mais {len(targets) - 10} targets")
    
    # Define portas para escanear
    common_ports = get_common_ports()
    ports = []
    
    if args.ports:
        ports.extend(expand_port_range(args.ports))
    if args.common_ports:
        if args.tcp:
            ports.extend(common_ports['tcp_common'])
        if args.udp:
            ports.extend(common_ports['udp_common'])
    if args.top100:
        ports.extend(common_ports['tcp_top100'])
    if args.top1000:
        ports.extend(common_ports['tcp_top1000'])
    
    ports = sorted(list(set(ports)))
    print(f"[+] Portas para escanear: {len(ports)}")
    
    if args.verbose:
        print(f"[+] Range de portas: {min(ports)}-{max(ports)}")
    
    # Define protocolos
    protocols = []
    if args.tcp:
        protocols.append('TCP')
    if args.udp:
        protocols.append('UDP')
    
    # Inicia varredura
    scanner = PortScanner(timeout=args.timeout, max_threads=args.threads)
    
    start_time = time.time()
    results = scanner.scan_range(targets, ports, protocols)
    end_time = time.time()
    
    # Exibe resultados
    scanner.display_results()
    
    print(f"\n[+] Varredura concluída em {end_time - start_time:.2f} segundos")
    
    # Salva resultados se solicitado
    if args.output:
        scanner.save_results(args.output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Varredura interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n[-] Erro: {e}")
        sys.exit(1)
