#!/usr/bin/env python3
"""
Exemplos de uso da ferramenta de varredura de portas
Execute este arquivo para testar as funcionalidades básicas
"""

import subprocess
import sys
import os

def run_command(description, command):
    """Executa um comando e exibe o resultado"""
    print(f"\n{'='*60}")
    print(f"EXEMPLO: {description}")
    print(f"COMANDO: {command}")
    print('='*60)
    
    try:
        # Executa o comando
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.stdout:
            print("SAÍDA:")
            print(result.stdout)
        
        if result.stderr:
            print("ERROS/AVISOS:")
            print(result.stderr)
            
        if result.returncode != 0:
            print(f"Comando falhou com código: {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("⏱️ Comando executado com timeout (>30s)")
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")

def main():
    """Executa exemplos de uso da ferramenta"""
    
    # Verifica se o arquivo principal existe
    scanner_path = "port_scanner.py"
    if not os.path.exists(scanner_path):
        print(f"❌ Arquivo {scanner_path} não encontrado!")
        print("Certifique-se de estar no diretório correto.")
        return
    
    print("🔍 DEMONSTRAÇÃO DA FERRAMENTA DE VARREDURA DE PORTAS")
    print("Este script demonstra várias funcionalidades da ferramenta")
    print("\n⚠️  AVISO: Os exemplos usarão localhost e IPs de exemplo.")
    print("Para uso em produção, substitua pelos seus targets reais.\n")
    
    input("Pressione ENTER para continuar...")
    
    # Lista de exemplos para demonstrar
    examples = [
        {
            "description": "Ajuda do programa",
            "command": f"python {scanner_path} --help"
        },
        {
            "description": "Scan básico TCP em localhost (portas comuns)",
            "command": f"python {scanner_path} -t 127.0.0.1 -p 80,443,22,21,25 --tcp"
        },
        {
            "description": "Scan de range de portas",
            "command": f"python {scanner_path} -t 127.0.0.1 -p 20-30 --tcp --timeout 1"
        },
        {
            "description": "Scan com portas comuns",
            "command": f"python {scanner_path} -t 127.0.0.1 --common-ports --tcp --timeout 1"
        },
        {
            "description": "Scan TCP e UDP",
            "command": f"python {scanner_path} -t 127.0.0.1 -p 53,80,443 --tcp --udp --timeout 2"
        },
        {
            "description": "Scan com saída verbosa",
            "command": f"python {scanner_path} -t 127.0.0.1 -p 80,8080 --tcp --verbose --timeout 1"
        },
        {
            "description": "Scan salvando em arquivo CSV",
            "command": f"python {scanner_path} -t 127.0.0.1 -p 22,80,443 --tcp -o exemplo_resultado.csv --timeout 1"
        }
    ]
    
    # Executa cada exemplo
    for i, example in enumerate(examples, 1):
        print(f"\n📋 EXECUTANDO EXEMPLO {i}/{len(examples)}")
        run_command(example["description"], example["command"])
        
        if i < len(examples):
            input("\nPressione ENTER para continuar para o próximo exemplo...")
    
    # Verifica se arquivo CSV foi criado
    csv_file = "exemplo_resultado.csv"
    if os.path.exists(csv_file):
        print(f"\n📄 CONTEÚDO DO ARQUIVO CSV GERADO ({csv_file}):")
        print("-" * 50)
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                print(f.read())
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
    
    print("\n✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print("\n📚 PRÓXIMOS PASSOS:")
    print("1. Leia o README.md para documentação completa")
    print("2. Teste com seus próprios targets (com autorização!)")
    print("3. Experimente diferentes configurações de timeout e threads")
    print("4. Use a opção --help para ver todos os parâmetros disponíveis")
    
    print("\n⚠️  LEMBRETE DE SEGURANÇA:")
    print("- Use apenas em redes próprias ou com autorização")
    print("- Respeite as leis locais sobre segurança cibernética")
    print("- Considere o impacto na rede ao fazer varreduras extensivas")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Demonstração interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante demonstração: {e}")
