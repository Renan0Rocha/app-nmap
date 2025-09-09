#!/usr/bin/env python3
"""
🎯 DEMONSTRAÇÃO COMPLETA - PORT SCANNER
Este script demonstra todas as funcionalidades do Port Scanner
"""

import subprocess
import sys
import time
import platform
from pathlib import Path

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_step(step, description):
    """Imprime passo da demonstração"""
    print(f"\n📍 PASSO {step}: {description}")
    print("-" * 40)

def run_command(cmd, description):
    """Executa comando e mostra resultado"""
    print(f"\n💻 Executando: {description}")
    print(f"📋 Comando: {cmd}")
    print("🔄 Aguarde...")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Sucesso!")
            if result.stdout:
                print("📄 Saída:")
                print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        else:
            print("❌ Erro!")
            print(f"💥 Código de erro: {result.returncode}")
            if result.stderr:
                print(f"⚠️ Erro: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - Comando demorou muito para executar")
    except Exception as e:
        print(f"💥 Erro inesperado: {e}")

def main():
    print_header("DEMONSTRAÇÃO COMPLETA DO PORT SCANNER")
    
    project_root = Path(__file__).parent
    print(f"📍 Diretório do projeto: {project_root}")
    print(f"🖥️ Sistema operacional: {platform.system()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Verificar arquivos principais
    print_step(1, "VERIFICAÇÃO DE ARQUIVOS")
    
    files_to_check = [
        "port_scanner.py",
        "gui_scanner.py", 
        "web_frontend/manage.py",
        "README.md",
        "requirements.txt"
    ]
    
    for file in files_to_check:
        file_path = project_root / file
        if file_path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - AUSENTE!")
    
    # Demonstração CLI
    print_step(2, "TESTE DA INTERFACE CLI")
    
    # Teste básico
    run_command(
        "python port_scanner.py 127.0.0.1 --ports 80,443 --timeout 2",
        "Teste básico - localhost portas 80,443"
    )
    
    # Teste com portas comuns
    run_command(
        "python port_scanner.py 8.8.8.8 --ports common --timeout 3",
        "Teste portas comuns - Google DNS"
    )
    
    # Demonstração GUI
    print_step(3, "TESTE DA INTERFACE GUI")
    
    print("🖼️ A interface GUI será aberta por 5 segundos...")
    print("💡 Feche a janela manualmente ou aguarde timeout")
    
    if platform.system() == "Windows":
        gui_cmd = "timeout /t 5 /nobreak > nul && taskkill /f /im python.exe > nul 2>&1 || python gui_scanner.py"
    else:
        gui_cmd = "timeout 5s python gui_scanner.py || true"
    
    run_command(gui_cmd, "Interface GUI (timeout 5s)")
    
    # Demonstração Web
    print_step(4, "TESTE DA INTERFACE WEB")
    
    print("🌐 Verificando se o Django está configurado...")
    
    web_dir = project_root / "web_frontend"
    if web_dir.exists():
        print("✅ Diretório web_frontend encontrado")
        
        # Testar import do Django
        run_command(
            "cd web_frontend && python -c \"import django; print('Django:', django.get_version())\"",
            "Verificação do Django"
        )
        
        # Verificar configuração
        run_command(
            "cd web_frontend && python manage.py check",
            "Verificação da configuração Django"
        )
        
        print("\n🌐 Para testar a interface web:")
        print("   1. cd web_frontend")
        print("   2. python manage.py runserver")
        print("   3. Acesse: http://localhost:8000")
        
    else:
        print("❌ Diretório web_frontend não encontrado!")
    
    # Demonstração de formatos de target
    print_step(5, "TESTE DE FORMATOS DE TARGET")
    
    targets_examples = [
        ("127.0.0.1", "IP único"),
        ("127.0.0.1,8.8.8.8", "Múltiplos IPs"),
        ("google.com", "Hostname"),
        ("127.0.0.1,google.com", "Misto")
    ]
    
    for target, description in targets_examples:
        run_command(
            f"python port_scanner.py {target} --ports 80 --timeout 2",
            f"Target: {description}"
        )
        time.sleep(1)
    
    # Testes de performance
    print_step(6, "TESTE DE PERFORMANCE")
    
    performance_tests = [
        ("--threads 10 --timeout 5", "Conservativo"),
        ("--threads 50 --timeout 3", "Moderado"),
        ("--threads 100 --timeout 1", "Agressivo")
    ]
    
    for params, mode in performance_tests:
        run_command(
            f"python port_scanner.py 127.0.0.1 --ports 21,22,23,25,53,80,110,443,993,995 {params}",
            f"Performance {mode}"
        )
        time.sleep(1)
    
    # Demonstração de exportação
    print_step(7, "TESTE DE EXPORTAÇÃO")
    
    export_formats = ["json", "txt", "csv"]
    
    for fmt in export_formats:
        output_file = f"demo_output.{fmt}"
        run_command(
            f"python port_scanner.py 127.0.0.1 --ports 80,443 --output {output_file} --format {fmt}",
            f"Exportação para {fmt.upper()}"
        )
        
        # Verificar se arquivo foi criado
        if (project_root / output_file).exists():
            print(f"✅ Arquivo {output_file} criado")
            # Mostrar conteúdo (primeiras linhas)
            try:
                with open(output_file, 'r') as f:
                    content = f.read()[:200]
                    print(f"📄 Preview: {content}...")
            except:
                pass
        else:
            print(f"❌ Arquivo {output_file} NÃO foi criado")
    
    # Resumo final
    print_header("DEMONSTRAÇÃO CONCLUÍDA")
    
    print("🎉 Todas as funcionalidades foram testadas!")
    print("\n📋 RESUMO DAS INTERFACES:")
    print("   🌐 Web Interface: cd web_frontend && python manage.py runserver")
    print("   🖼️ GUI Interface: python gui_scanner.py")
    print("   ⌨️ CLI Interface: python port_scanner.py --help")
    
    print("\n💡 EXEMPLOS PRÁTICOS:")
    print("   # Rede local completa")
    print("   python port_scanner.py 192.168.1.0/24 --ports common")
    print("")
    print("   # Alta performance")
    print("   python port_scanner.py TARGET --threads 200 --timeout 1")
    print("")
    print("   # UDP scan")
    print("   python port_scanner.py 8.8.8.8 --ports 53 --protocol udp")
    
    print("\n⚖️ LEMBRE-SE:")
    print("   ✅ Use apenas em redes autorizadas")
    print("   ✅ Respeite rate limits")
    print("   ✅ Use com responsabilidade")
    
    print(f"\n📁 Projeto disponível em: {project_root}")
    print("📖 Consulte README_COMPLETE.md para documentação completa")
    
    print("\n" + "="*60)
    print("🛡️ DEMONSTRAÇÃO FINALIZADA - USE COM RESPONSABILIDADE!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demonstração cancelada pelo usuário!")
    except Exception as e:
        print(f"\n\n💥 Erro na demonstração: {e}")
        print("📞 Reporte este erro se necessário")
