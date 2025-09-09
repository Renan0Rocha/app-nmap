#!/usr/bin/env python3
"""
Script de instalação e verificação da ferramenta de varredura de portas
"""

import sys
import os
import subprocess
import platform


def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("❌ Python 3.6+ é necessário")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatível")
    return True


def check_permissions():
    """Verifica permissões necessárias"""
    system = platform.system().lower()
    
    if system == "windows":
        # No Windows, verifica se está executando como administrador
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if is_admin:
                print("✅ Executando com privilégios administrativos")
            else:
                print("⚠️  Não está executando como administrador")
                print("   Algumas funcionalidades UDP podem não funcionar corretamente")
        except:
            print("⚠️  Não foi possível verificar privilégios")
    
    elif system in ["linux", "darwin"]:  # Linux ou macOS
        uid = os.getuid()
        if uid == 0:
            print("✅ Executando com privilégios root")
        else:
            print("⚠️  Não está executando como root")
            print("   Algumas funcionalidades avançadas podem não funcionar")
    
    return True


def test_network_access():
    """Testa acesso à rede"""
    try:
        import socket
        
        # Testa conexão TCP local
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 80))
        sock.close()
        
        print("✅ Acesso à rede local funcional")
        
        # Testa resolução DNS
        socket.gethostbyname('google.com')
        print("✅ Resolução DNS funcional")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Problema de rede detectado: {e}")
        return False


def check_required_modules():
    """Verifica se todos os módulos necessários estão disponíveis"""
    required_modules = [
        'socket', 'threading', 'time', 'argparse', 'ipaddress',
        'concurrent.futures', 'dataclasses', 'struct', 'sys'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - AUSENTE")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Módulos ausentes: {', '.join(missing_modules)}")
        return False
    
    print("✅ Todos os módulos necessários estão disponíveis")
    return True


def check_optional_modules():
    """Verifica módulos opcionais para funcionalidades extras"""
    optional_modules = {
        'tkinter': 'Interface gráfica',
        'scapy': 'Funcionalidades avançadas de rede',
        'psutil': 'Informações do sistema',
        'colorama': 'Saída colorida no terminal'
    }
    
    print("\n📦 MÓDULOS OPCIONAIS:")
    
    for module, description in optional_modules.items():
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"⚪ {module} - {description} (não instalado)")


def test_scanner_basic():
    """Testa funcionalidades básicas do scanner"""
    print("\n🧪 TESTANDO FUNCIONALIDADES BÁSICAS:")
    
    try:
        # Importa o scanner
        from port_scanner import PortScanner, expand_cidr, expand_port_range
        print("✅ Importação do módulo principal")
        
        # Testa expansão CIDR
        result = expand_cidr("127.0.0.1")
        assert result == ["127.0.0.1"]
        print("✅ Expansão CIDR")
        
        # Testa expansão de portas
        result = expand_port_range("80,443")
        assert set(result) == {80, 443}
        print("✅ Expansão de portas")
        
        # Testa criação do scanner
        scanner = PortScanner(timeout=1, max_threads=10)
        print("✅ Criação do scanner")
        
        # Testa scan básico
        result = scanner.scan_tcp_port("127.0.0.1", 65432)  # Porta provavelmente fechada
        assert result.host == "127.0.0.1"
        assert result.port == 65432
        assert result.protocol == "TCP"
        print("✅ Scan TCP básico")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def create_desktop_shortcut():
    """Cria atalho na área de trabalho (Windows)"""
    if platform.system().lower() != "windows":
        return
    
    try:
        import win32com.client
        
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "Port Scanner.lnk")
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = os.path.join(os.getcwd(), "port_scanner.py")
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print("✅ Atalho criado na área de trabalho")
        
    except ImportError:
        print("⚪ pywin32 não instalado - atalho não criado")
    except Exception as e:
        print(f"⚠️  Erro ao criar atalho: {e}")


def show_usage_examples():
    """Mostra exemplos de uso"""
    print("\n📚 EXEMPLOS DE USO:")
    print("-" * 50)
    
    examples = [
        ("Scan básico TCP", "python port_scanner.py -t 192.168.1.1 -p 80,443"),
        ("Scan de rede", "python port_scanner.py -t 192.168.1.0/24 -p 22,80,443"),
        ("Portas comuns", "python port_scanner.py -t 10.0.0.1 --common-ports --tcp"),
        ("TCP e UDP", "python port_scanner.py -t example.com -p 53,80 --tcp --udp"),
        ("Salvar resultado", "python port_scanner.py -t 127.0.0.1 -p 80-90 -o resultado.csv"),
        ("Interface gráfica", "python gui_scanner.py"),
        ("Executar testes", "python test_scanner.py"),
        ("Ver demonstração", "python exemplo_uso.py")
    ]
    
    for description, command in examples:
        print(f"  {description:15} : {command}")


def main():
    """Função principal de instalação e verificação"""
    print("🔧 INSTALAÇÃO E VERIFICAÇÃO - FERRAMENTA DE VARREDURA DE PORTAS")
    print("=" * 70)
    
    # Informações do sistema
    print(f"\n💻 SISTEMA: {platform.system()} {platform.release()}")
    print(f"🐍 PYTHON: {platform.python_version()}")
    print(f"📁 DIRETÓRIO: {os.getcwd()}")
    
    # Lista de verificações
    checks = [
        ("Versão do Python", check_python_version),
        ("Permissões do sistema", check_permissions),
        ("Módulos necessários", check_required_modules),
        ("Acesso à rede", test_network_access),
        ("Funcionalidades básicas", test_scanner_basic)
    ]
    
    print("\n🔍 EXECUTANDO VERIFICAÇÕES:")
    print("-" * 40)
    
    all_passed = True
    
    for description, check_func in checks:
        print(f"\n[{description}]")
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Erro durante verificação: {e}")
            all_passed = False
    
    # Verifica módulos opcionais
    check_optional_modules()
    
    # Cria atalho se possível
    if platform.system().lower() == "windows":
        print("\n🔗 CRIANDO ATALHO:")
        create_desktop_shortcut()
    
    # Resultado final
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("\n🎉 A ferramenta está pronta para uso!")
        
        # Mostra próximos passos
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Leia o README.md para documentação completa")
        print("2. Execute 'python exemplo_uso.py' para ver demonstrações")
        print("3. Execute 'python test_scanner.py' para testes detalhados")
        print("4. Use 'python port_scanner.py --help' para ver todas as opções")
        
        if os.path.exists("gui_scanner.py"):
            print("5. Execute 'python gui_scanner.py' para interface gráfica")
        
    else:
        print("⚠️  INSTALAÇÃO CONCLUÍDA COM PROBLEMAS")
        print("\nAlgumas funcionalidades podem não funcionar corretamente.")
        print("Verifique os erros acima e resolva os problemas identificados.")
    
    # Mostra exemplos de uso
    show_usage_examples()
    
    print("\n⚠️  LEMBRETE LEGAL:")
    print("Use esta ferramenta apenas em redes próprias ou com autorização.")
    print("O uso não autorizado pode violar leis locais de segurança cibernética.")
    
    return all_passed


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Instalação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante instalação: {e}")
        sys.exit(1)
