#!/usr/bin/env python3
"""
Port Scanner - Instalador Automático Aprimorado
Instala e configura automaticamente o ambiente para o Port Scanner
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class PortScannerInstaller:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.system = platform.system().lower()
        
    def print_header(self):
        """Imprime cabeçalho do instalador"""
        print("\n" + "="*60)
        print("🔍 PORT SCANNER - INSTALADOR AUTOMÁTICO")
        print("="*60)
        print(f"📍 Diretório: {self.project_root}")
        print(f"🖥️  Sistema: {platform.system()} {platform.release()}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print("="*60 + "\n")
        
    def check_python_version(self):
        """Verifica versão do Python"""
        print("🔍 Verificando versão do Python...")
        
        if sys.version_info < (3, 8):
            print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} não suportado!")
            print("📋 Requisito mínimo: Python 3.8+")
            print("📁 Download: https://python.org/downloads/")
            sys.exit(1)
            
        print(f"✅ Python {sys.version.split()[0]} - OK")
        
    def check_dependencies(self):
        """Verifica dependências do sistema"""
        print("\n🔍 Verificando dependências...")
        
        # Verificar pip
        try:
            import pip
            print("✅ pip - OK")
        except ImportError:
            print("❌ pip não encontrado!")
            sys.exit(1)
            
        # Verificar venv
        try:
            import venv
            print("✅ venv - OK")
        except ImportError:
            print("❌ venv não encontrado!")
            sys.exit(1)
    
    def create_virtual_environment(self):
        """Cria ambiente virtual"""
        print("\n📦 Configurando ambiente virtual...")
        
        if self.venv_path.exists():
            print("🔄 Ambiente virtual já existe, recriando...")
            shutil.rmtree(self.venv_path)
            
        try:
            subprocess.run([
                sys.executable, "-m", "venv", str(self.venv_path)
            ], check=True, capture_output=True, text=True)
            print("✅ Ambiente virtual criado")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao criar ambiente virtual: {e}")
            sys.exit(1)
    
    def get_pip_executable(self):
        """Retorna caminho do pip no ambiente virtual"""
        if self.system == "windows":
            return self.venv_path / "Scripts" / "pip.exe"
        else:
            return self.venv_path / "bin" / "pip"
    
    def install_requirements(self):
        """Instala dependências Python"""
        print("\n📋 Instalando dependências...")
        
        pip_exe = self.get_pip_executable()
        
        # Atualizar pip
        print("🔧 Atualizando pip...")
        try:
            subprocess.run([
                str(pip_exe), "install", "--upgrade", "pip"
            ], check=True, capture_output=True, text=True)
            print("✅ pip atualizado")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Aviso: Erro ao atualizar pip: {e}")
        
        # Instalar requirements.txt
        requirements_file = self.project_root / "requirements.txt"
        if requirements_file.exists():
            print("📋 Instalando requirements.txt...")
            try:
                subprocess.run([
                    str(pip_exe), "install", "-r", str(requirements_file)
                ], check=True, capture_output=True, text=True)
                print("✅ Dependências principais instaladas")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao instalar requirements.txt: {e}")
                sys.exit(1)
        
        # Instalar requirements web
        web_requirements = self.project_root / "web_frontend" / "requirements_web.txt"
        if web_requirements.exists():
            print("🌐 Instalando dependências web...")
            try:
                subprocess.run([
                    str(pip_exe), "install", "-r", str(web_requirements)
                ], check=True, capture_output=True, text=True)
                print("✅ Dependências web instaladas")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Aviso: Erro ao instalar requirements web: {e}")
    
    def setup_django(self):
        """Configura Django"""
        print("\n🗄️ Configurando Django...")
        
        python_exe = self.get_python_executable()
        web_dir = self.project_root / "web_frontend"
        
        if not web_dir.exists():
            print("⚠️ Diretório web_frontend não encontrado, pulando configuração Django")
            return
            
        try:
            # makemigrations
            print("📋 Criando migrações...")
            subprocess.run([
                str(python_exe), "manage.py", "makemigrations"
            ], cwd=str(web_dir), check=True, capture_output=True, text=True)
            
            # migrate
            print("🗄️ Aplicando migrações...")
            subprocess.run([
                str(python_exe), "manage.py", "migrate"
            ], cwd=str(web_dir), check=True, capture_output=True, text=True)
            
            print("✅ Django configurado")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Aviso: Erro na configuração Django: {e}")
    
    def get_python_executable(self):
        """Retorna caminho do Python no ambiente virtual"""
        if self.system == "windows":
            return self.venv_path / "Scripts" / "python.exe"
        else:
            return self.venv_path / "bin" / "python"
    
    def create_startup_scripts(self):
        """Cria scripts de inicialização"""
        print("\n🚀 Criando scripts de inicialização...")
        
        if self.system == "windows":
            self.create_windows_scripts()
        else:
            self.create_unix_scripts()
            
        print("✅ Scripts criados")
    
    def create_windows_scripts(self):
        """Cria scripts para Windows"""
        # Script para web
        web_script = self.project_root / "RUN_WEB.bat"
        with open(web_script, 'w', encoding='utf-8') as f:
            f.write(f"""@echo off
title Port Scanner - Web Interface
cd /d "{self.project_root}"
call venv\\Scripts\\activate.bat
cd web_frontend
python manage.py runserver
pause
""")
        
        # Script para GUI  
        gui_script = self.project_root / "RUN_GUI.bat"
        with open(gui_script, 'w', encoding='utf-8') as f:
            f.write(f"""@echo off
title Port Scanner - GUI Interface  
cd /d "{self.project_root}"
call venv\\Scripts\\activate.bat
python gui_scanner.py
pause
""")
    
    def create_unix_scripts(self):
        """Cria scripts para Unix/Linux/macOS"""
        # Script para web
        web_script = self.project_root / "run_web.sh"
        with open(web_script, 'w') as f:
            f.write(f"""#!/bin/bash
cd "{self.project_root}"
source venv/bin/activate
cd web_frontend
python manage.py runserver
""")
        web_script.chmod(0o755)
        
        # Script para GUI
        gui_script = self.project_root / "run_gui.sh"
        with open(gui_script, 'w') as f:
            f.write(f"""#!/bin/bash
cd "{self.project_root}"
source venv/bin/activate
python gui_scanner.py
""")
        gui_script.chmod(0o755)
    
    def show_completion_message(self):
        """Mostra mensagem de conclusão"""
        print("\n" + "="*60)
        print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print("\n📋 COMO USAR:")
        print("┌─────────────────────────────────────────────────┐")
        print("│  🌐 INTERFACE WEB (Recomendada)                │")
        
        if self.system == "windows":
            print("│     Clique duplo: RUN_WEB.bat                  │")
        else:
            print("│     Execute: ./run_web.sh                      │")
        
        print("│     Ou: cd web_frontend && python manage.py runserver │")
        print("│     Acesse: http://localhost:8000              │")
        print("├─────────────────────────────────────────────────┤")
        print("│  🖼️ INTERFACE GUI                               │")
        
        if self.system == "windows":
            print("│     Clique duplo: RUN_GUI.bat                  │")
        else:
            print("│     Execute: ./run_gui.sh                      │")
            
        print("│     Ou: python gui_scanner.py                  │")
        print("├─────────────────────────────────────────────────┤")
        print("│  ⌨️ LINHA DE COMANDO                            │")
        print("│     python port_scanner.py --help             │")
        print("└─────────────────────────────────────────────────┘")
        
        print("\n💡 EXEMPLOS RÁPIDOS:")
        print("   python port_scanner.py 192.168.1.1 --ports common")
        print("   python port_scanner.py 192.168.1.0/24 --ports 1-1000")
        
        print(f"\n📁 Projeto instalado em: {self.project_root}")
        print("📖 Consulte README_COMPLETE.md para documentação completa")
        print("\n⚖️ USE APENAS EM REDES AUTORIZADAS! 🛡️")
        print("="*60 + "\n")
    
    def install(self):
        """Executa instalação completa"""
        try:
            self.print_header()
            self.check_python_version()
            self.check_dependencies()
            self.create_virtual_environment()
            self.install_requirements()
            self.setup_django()
            self.create_startup_scripts()
            self.show_completion_message()
            
        except KeyboardInterrupt:
            print("\n\n❌ Instalação cancelada pelo usuário!")
            sys.exit(1)
        except Exception as e:
            print(f"\n\n💥 Erro inesperado: {e}")
            print("📞 Reporte este erro para suporte")
            sys.exit(1)

def main():
    installer = PortScannerInstaller()
    installer.install()

if __name__ == "__main__":
    main()
