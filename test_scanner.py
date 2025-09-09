#!/usr/bin/env python3
"""
Script de teste para verificar funcionalidades da ferramenta de varredura
"""

import unittest
import socket
import threading
import time
import tempfile
import os
from port_scanner import PortScanner, ScanResult, expand_cidr, expand_port_range, get_common_ports


class TestPortScanner(unittest.TestCase):
    """Testes unitários para o PortScanner"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.scanner = PortScanner(timeout=1, max_threads=10)
        self.test_host = "127.0.0.1"
    
    def test_expand_cidr(self):
        """Testa expansão de notação CIDR"""
        # Teste IP único
        result = expand_cidr("192.168.1.1")
        self.assertEqual(result, ["192.168.1.1"])
        
        # Teste CIDR pequeno
        result = expand_cidr("192.168.1.0/30")
        expected = ["192.168.1.1", "192.168.1.2"]  # .0 e .3 são network e broadcast
        self.assertEqual(result, expected)
    
    def test_expand_port_range(self):
        """Testa expansão de ranges de portas"""
        # Teste portas individuais
        result = expand_port_range("80,443")
        self.assertEqual(result, [80, 443])
        
        # Teste range
        result = expand_port_range("20-22")
        self.assertEqual(result, [20, 21, 22])
        
        # Teste misto
        result = expand_port_range("80,90-92,443")
        expected = [80, 90, 91, 92, 443]
        self.assertEqual(result, expected)
    
    def test_get_common_ports(self):
        """Testa obtenção de portas comuns"""
        ports = get_common_ports()
        
        # Verifica se contém as chaves esperadas
        self.assertIn('tcp_common', ports)
        self.assertIn('udp_common', ports)
        self.assertIn('tcp_top100', ports)
        self.assertIn('tcp_top1000', ports)
        
        # Verifica se portas comuns estão presentes
        self.assertIn(80, ports['tcp_common'])  # HTTP
        self.assertIn(443, ports['tcp_common']) # HTTPS
        self.assertIn(53, ports['udp_common'])  # DNS
    
    def test_scan_result_creation(self):
        """Testa criação de objetos ScanResult"""
        result = ScanResult("127.0.0.1", 80, "TCP", "open")
        
        self.assertEqual(result.host, "127.0.0.1")
        self.assertEqual(result.port, 80)
        self.assertEqual(result.protocol, "TCP")
        self.assertEqual(result.status, "open")
    
    def test_tcp_scan_closed_port(self):
        """Testa scan TCP em porta fechada"""
        # Usa uma porta que provavelmente está fechada
        result = self.scanner.scan_tcp_port(self.test_host, 65432)
        
        # Deve ser fechada ou filtrada
        self.assertIn(result.status, ['closed', 'filtered'])
        self.assertEqual(result.protocol, 'TCP')
        self.assertEqual(result.host, self.test_host)
        self.assertEqual(result.port, 65432)
    
    def test_save_results(self):
        """Testa salvamento de resultados"""
        # Cria alguns resultados de teste
        self.scanner.results = [
            ScanResult("127.0.0.1", 80, "TCP", "open"),
            ScanResult("127.0.0.1", 443, "TCP", "closed")
        ]
        
        # Salva em arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_name = tmp.name
        
        try:
            self.scanner.save_results(tmp_name)
            
            # Verifica se arquivo foi criado e tem conteúdo correto
            self.assertTrue(os.path.exists(tmp_name))
            
            with open(tmp_name, 'r') as f:
                content = f.read()
                self.assertIn("Host,Port,Protocol,Status", content)
                self.assertIn("127.0.0.1,80,TCP,open", content)
                self.assertIn("127.0.0.1,443,TCP,closed", content)
        finally:
            # Limpa arquivo temporário
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)


class TestServerForTesting:
    """Servidor simples para testes"""
    
    def __init__(self, port, protocol='TCP'):
        self.port = port
        self.protocol = protocol
        self.running = False
        self.thread = None
        self.socket = None
    
    def start(self):
        """Inicia o servidor de teste"""
        if self.running:
            return
        
        self.running = True
        if self.protocol == 'TCP':
            self.thread = threading.Thread(target=self._tcp_server, daemon=True)
        else:
            self.thread = threading.Thread(target=self._udp_server, daemon=True)
        
        self.thread.start()
        time.sleep(0.1)  # Aguarda servidor iniciar
    
    def stop(self):
        """Para o servidor de teste"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
    
    def _tcp_server(self):
        """Servidor TCP simples"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(("127.0.0.1", self.port))
            self.socket.listen(1)
            self.socket.settimeout(1)
            
            while self.running:
                try:
                    conn, addr = self.socket.accept()
                    conn.close()
                except socket.timeout:
                    continue
                except:
                    break
        except Exception as e:
            print(f"Erro no servidor TCP: {e}")
    
    def _udp_server(self):
        """Servidor UDP simples"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(("127.0.0.1", self.port))
            self.socket.settimeout(1)
            
            while self.running:
                try:
                    data, addr = self.socket.recvfrom(1024)
                    # Responde para indicar que porta está aberta
                    self.socket.sendto(b"OK", addr)
                except socket.timeout:
                    continue
                except:
                    break
        except Exception as e:
            print(f"Erro no servidor UDP: {e}")


class TestIntegration(unittest.TestCase):
    """Testes de integração com servidor real"""
    
    def setUp(self):
        """Configuração inicial dos testes de integração"""
        self.scanner = PortScanner(timeout=2, max_threads=5)
        self.test_servers = []
    
    def tearDown(self):
        """Limpeza após testes"""
        for server in self.test_servers:
            server.stop()
    
    def test_tcp_scan_open_port(self):
        """Testa scan TCP em porta aberta"""
        # Inicia servidor de teste
        server = TestServerForTesting(12345, 'TCP')
        server.start()
        self.test_servers.append(server)
        
        # Escaneia a porta
        result = self.scanner.scan_tcp_port("127.0.0.1", 12345)
        
        # Verifica resultado
        self.assertEqual(result.status, "open")
        self.assertEqual(result.protocol, "TCP")
    
    def test_udp_scan_open_port(self):
        """Testa scan UDP em porta aberta"""
        # Inicia servidor de teste
        server = TestServerForTesting(12346, 'UDP')
        server.start()
        self.test_servers.append(server)
        
        # Escaneia a porta
        result = self.scanner.scan_udp_port("127.0.0.1", 12346)
        
        # Para UDP, pode ser "open" ou "open|filtered"
        self.assertIn("open", result.status)
        self.assertEqual(result.protocol, "UDP")
    
    def test_scan_range_integration(self):
        """Testa varredura de range completa"""
        # Inicia alguns servidores
        tcp_server = TestServerForTesting(12347, 'TCP')
        udp_server = TestServerForTesting(12348, 'UDP')
        
        tcp_server.start()
        udp_server.start()
        
        self.test_servers.extend([tcp_server, udp_server])
        
        # Escaneia range incluindo portas abertas e fechadas
        hosts = ["127.0.0.1"]
        ports = [12347, 12348, 12349]  # Uma TCP aberta, uma UDP aberta, uma fechada
        protocols = ["TCP", "UDP"]
        
        results = self.scanner.scan_range(hosts, ports, protocols)
        
        # Verifica se obteve resultados
        self.assertTrue(len(results) > 0)
        
        # Verifica se encontrou pelo menos uma porta aberta
        open_results = [r for r in results if "open" in r.status]
        self.assertTrue(len(open_results) > 0)


def run_performance_test():
    """Executa teste de performance"""
    print("\n" + "="*60)
    print("TESTE DE PERFORMANCE")
    print("="*60)
    
    scanner = PortScanner(timeout=1, max_threads=50)
    
    # Teste 1: Scan local pequeno
    print("\n[1] Teste: Scan local (10 portas TCP)")
    start_time = time.time()
    
    results = scanner.scan_range(
        hosts=["127.0.0.1"],
        ports=list(range(8000, 8010)),
        protocols=["TCP"]
    )
    
    end_time = time.time()
    print(f"    Tempo: {end_time - start_time:.2f}s")
    print(f"    Resultados: {len(results)}")
    
    # Teste 2: Scan com threads diferentes
    print("\n[2] Teste: Comparação de threads")
    
    for thread_count in [10, 50, 100]:
        scanner_test = PortScanner(timeout=1, max_threads=thread_count)
        
        start_time = time.time()
        results = scanner_test.scan_range(
            hosts=["127.0.0.1"],
            ports=list(range(9000, 9020)),
            protocols=["TCP"]
        )
        end_time = time.time()
        
        print(f"    {thread_count} threads: {end_time - start_time:.2f}s ({len(results)} resultados)")


def main():
    """Executa todos os testes"""
    print("🧪 EXECUTANDO TESTES DA FERRAMENTA DE VARREDURA")
    print("="*60)
    
    # Executa testes unitários
    print("\n[+] Executando testes unitários...")
    unittest.main(argv=[''], exit=False, verbosity=2, 
                 testRunner=unittest.TextTestRunner(stream=None))
    
    # Executa teste de performance
    try:
        run_performance_test()
    except Exception as e:
        print(f"\n❌ Erro no teste de performance: {e}")
    
    print("\n✅ Testes concluídos!")
    print("\n📋 INTERPRETAÇÃO DOS RESULTADOS:")
    print("- OK: Teste passou com sucesso")
    print("- FAIL: Teste falhou - verificar implementação")
    print("- ERROR: Erro durante execução do teste")
    print("\n💡 DICA: Execute 'python test_scanner.py' para testes detalhados")


if __name__ == "__main__":
    main()
