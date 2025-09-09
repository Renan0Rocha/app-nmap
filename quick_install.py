#!/usr/bin/env python3
"""
Instalador Rápido do Port Scanner
Versão simplificada para instalação básica
"""

import os
import sys
import subprocess
import platform

def main():
    print("🔍 PORT SCANNER - INSTALAÇÃO RÁPIDA")
    print("=" * 50)
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ ERRO: Python 3.8+ é necessário")
        print(f"   Versão atual: {sys.version.split()[0]}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} - Compatível")
    
    # Instalar dependências principais
    print("\n📦 Instalando dependências principais...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências principais instaladas")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências principais")
        sys.exit(1)
    
    # Instalar dependências web
    web_dir = "web_frontend"
    if os.path.exists(f"{web_dir}/requirements_web.txt"):
        print("\n🌐 Instalando dependências da interface web...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", f"{web_dir}/requirements_web.txt"], check=True)
            print("✅ Interface web configurada")
            
            # Configurar Django
            print("⚙️ Configurando Django...")
            original_dir = os.getcwd()
            os.chdir(web_dir)
            
            subprocess.run([sys.executable, "manage.py", "migrate"], check=True, capture_output=True)
            os.chdir(original_dir)
            print("✅ Django configurado")
            
        except subprocess.CalledProcessError:
            print("⚠️ Erro na configuração web (não crítico)")
    
    # Criar arquivo batch para Windows
    if platform.system() == "Windows":
        print("\n📝 Criando arquivo de conveniência...")
        web_batch = """@echo off
echo 🌐 Port Scanner - Interface Web
echo Iniciando servidor...
cd web_frontend
python manage.py runserver 8000
echo.
echo Acesse: http://localhost:8000
pause
"""
        with open("start_web.bat", "w") as f:
            f.write(web_batch)
        print("✅ Arquivo start_web.bat criado")
    
    # Instruções finais
    print("\n" + "=" * 50)
    print("🎉 INSTALAÇÃO CONCLUÍDA!")
    print("=" * 50)
    print("\n🚀 COMO USAR:")
    print("\n1️⃣ Interface Web (Recomendada):")
    print("   cd web_frontend")
    print("   python manage.py runserver")
    print("   🌐 http://localhost:8000")
    
    if platform.system() == "Windows":
        print("\n🪟 Windows: Clique duplo em start_web.bat")
    
    print("\n2️⃣ Interface CLI:")
    print("   python port_scanner.py 192.168.1.1 --ports 80,443")
    
    print("\n3️⃣ Interface GUI:")
    print("   python gui_scanner.py")
    
    print("\n📚 Documentação: README_COMPLETE.md")

if __name__ == "__main__":
    main()
