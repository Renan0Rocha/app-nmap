# 🔍 Port Scanner - Ferramenta de Varredura TCP/UDP

Ferramenta completa de varredura de portas desenvolvida em Python com três interfaces distintas: Web, GUI e CLI.

## 🚀 Instalação e Execução Rápida

### 1. Instalação Automática
```bash
python install_complete.py
```

### 2. Executar Interface Web (Recomendada)
```bash
cd web_frontend
python manage.py runserver
```
🌐 **Acesse: http://localhost:8000**

### 3. Windows - Clique Duplo
- `setup_and_start_web.bat` - Interface Web
- `setup_and_start_gui.bat` - Interface GUI

## ✨ Características Principais

- ✅ **Varredura TCP/UDP** - Protocolos completos
- ✅ **Múltiplos alvos** - IP único, múltiplos IPs, CIDR, hostnames  
- ✅ **3 Interfaces** - Web moderna, GUI desktop, CLI para automação
- ✅ **Multi-threading** - Performance otimizada
- ✅ **Exportação** - JSON, TXT, CSV
- ✅ **Cross-platform** - Windows, Linux, macOS

## � Interfaces Disponíveis

| Interface | Como Executar | Melhor Para |
|-----------|---------------|-------------|
| 🌐 **Web** | `cd web_frontend && python manage.py runserver` | Uso geral, múltiplos usuários |
| 🖼️ **GUI** | `python gui_scanner.py` | Usuários desktop |
| ⌨️ **CLI** | `python port_scanner.py TARGET --ports PORTAS` | Automação, scripts |

## 🎯 Formatos de Target Suportados

```bash
# IP único
192.168.1.1

# Múltiplos IPs
192.168.1.1,192.168.1.10,192.168.1.20

# Rede completa (CIDR)
192.168.1.0/24

# Hostnames
google.com,github.com

# Misto
127.0.0.1,192.168.1.0/28,google.com
```

## ⚡ Exemplos Rápidos

```bash
# Portas comuns em IP local
python port_scanner.py 192.168.1.1 --ports common

# Múltiplos alvos  
python port_scanner.py 192.168.1.1,google.com --ports 22,80,443

# Rede completa
python port_scanner.py 192.168.1.0/24 --ports 1-1000 --threads 100

# UDP
python port_scanner.py 8.8.8.8 --ports 53 --protocol udp

# Alta performance
python port_scanner.py 192.168.1.0/24 --ports common --threads 200 --timeout 1

# Salvar resultados
python port_scanner.py 192.168.1.1 --ports 1-65535 --output scan.json --format json
```
- **Histórico** e **análise** de varreduras
- **Export** de dados (JSON, CSV)
- **Administração** via Django Admin

## ✨ Características Principais

- ✅ **Varredura TCP/UDP** com detecção precisa de status
- ✅ **Múltiplos targets** (IP, CIDR, hostname, listas)
- ✅ **Threading otimizado** para alta performance  
- ✅ **Detecção de serviços** e banner grabbing
- ✅ **Configuração flexível** de portas e timeouts
- ✅ **Interface web moderna** com tempo real
- ✅ **API REST** para automação e integração

## Requisitos

- Python 3.6+
- Bibliotecas padrão do Python (socket, threading, argparse, etc.)
- Permissões de administrador podem ser necessárias para algumas funcionalidades UDP

## Instalação

```bash
# Clone ou baixe o arquivo port_scanner.py
# Não são necessárias dependências externas
```

## Uso Básico

### Exemplos Simples

```bash
# Escanear portas TCP específicas
python port_scanner.py -t 192.168.1.1 -p 80,443,8080

# Escanear range de portas
python port_scanner.py -t 192.168.1.1 -p 1-1000 --tcp

# Escanear portas comuns
python port_scanner.py -t 192.168.1.1 --common-ports --tcp

# Escanear top 100 portas
python port_scanner.py -t 192.168.1.1 --top100
```

### Exemplos Avançados

```bash
# Escanear rede inteira (CIDR)
python port_scanner.py -t 192.168.1.0/24 -p 22,80,443 --tcp

# Escanear múltiplos IPs específicos
python port_scanner.py -t 192.168.1.1,192.168.1.137,192.168.1.234 -p 22,80,443,3000 --tcp

# Escanear TCP e UDP
python port_scanner.py -t 10.0.0.1 -p 53,80,443 --tcp --udp

# Configurar timeout e threads
python port_scanner.py -t example.com -p 1-100 --timeout 5 --threads 50

# Salvar resultados em arquivo
python port_scanner.py -t 192.168.1.1 --common-ports --tcp -o resultados.csv

# Modo verboso
python port_scanner.py -t 192.168.1.1 -p 80-90 --tcp --verbose
```

## Parâmetros

### Obrigatórios
- `-t, --target`: IP, hostname ou CIDR do destino

### Portas
- `-p, --ports`: Portas específicas (ex: 80,443 ou 1-1000)
- `--common-ports`: Escanear portas comuns
- `--top100`: Escanear top 100 portas TCP
- `--top1000`: Escanear top 1000 portas TCP

### Protocolos
- `--tcp`: Escanear portas TCP (padrão se nenhum protocolo especificado)
- `--udp`: Escanear portas UDP

### Configurações
- `--timeout`: Timeout por conexão (padrão: 3s)
- `--threads`: Número máximo de threads (padrão: 100)
- `-o, --output`: Arquivo para salvar resultados (formato CSV)
- `--verbose`: Saída detalhada

## Interpretação dos Resultados

### Status das Portas

- **OPEN**: Porta aberta e aceitando conexões
- **CLOSED**: Porta fechada (resposta de recusa ativa)
- **FILTERED**: Porta filtrada (firewall/filtros de rede)
- **OPEN|FILTERED**: (UDP) Porta possivelmente aberta ou filtrada

### Exemplo de Saída

```
[+] Iniciando varredura de 1 host(s) em 20 porta(s)
[+] Protocolos: TCP
[+] Timeout: 3s | Max Threads: 100
------------------------------------------------------------
[+] Progresso: 20/20 (100.0%)

============================================================
RESULTADOS DA VARREDURA
============================================================

[+] PORTAS ABERTAS (3):
    192.168.1.1:22/TCP - OPEN
    192.168.1.1:80/TCP - OPEN
    192.168.1.1:443/TCP - OPEN

[-] PORTAS FECHADAS (15):
    192.168.1.1:21/TCP - CLOSED
    192.168.1.1:23/TCP - CLOSED
    ...

[!] PORTAS FILTRADAS (2):
    192.168.1.1:135/TCP - FILTERED
    192.168.1.1:139/TCP - FILTERED

[*] Total de portas escaneadas: 20
[+] Varredura concluída em 2.34 segundos
```

## Técnicas Implementadas

### TCP Scanning
- **Método**: Connect Scan (TCP Three-way Handshake)
- **Funcionamento**: Tenta estabelecer conexão TCP completa
- **Vantagens**: Simples, confiável, não requer privilégios especiais
- **Detecção**: 
  - OPEN: Conexão estabelecida com sucesso
  - CLOSED: Conexão recusada (RST packet)
  - FILTERED: Timeout (firewall/filtros)

### UDP Scanning
- **Método**: UDP Probe
- **Funcionamento**: Envia pacotes UDP e analisa respostas ICMP
- **Detecção**:
  - OPEN|FILTERED: Sem resposta ICMP (pode estar aberta ou filtrada)
  - CLOSED: ICMP Port Unreachable
  - FILTERED: Outros erros de rede

## Performance

### Otimizações Implementadas
- **Threading**: Execução paralela de múltiplas verificações
- **Connection Pooling**: Reutilização de recursos de rede
- **Timeout Configurável**: Balanceamento entre velocidade e precisão
- **Progress Tracking**: Monitoramento do progresso da varredura

### Recomendações de Performance
- Para redes locais: `--threads 200 --timeout 1`
- Para redes remotas: `--threads 50 --timeout 5`
- Para varreduras stealth: `--threads 10 --timeout 10`

## 📚 Documentação

- **README_COMPLETE.md** - Documentação completa
- **INSTALL.md** - Guia de instalação detalhado
- **ARCHITECTURE.py** - Arquitetura do projeto

## 🛠️ Dependências

```bash
# Principais
pip install -r requirements.txt

# Interface Web
pip install -r web_frontend/requirements_web.txt
```

## ⚖️ Aviso Legal

⚠️ **Use apenas em:**
- ✅ Redes próprias
- ✅ Sistemas autorizados  
- ✅ Ambientes de teste

❌ **Não use para atividades maliciosas ou não autorizadas**

---

**Desenvolvido para fins educacionais e de segurança. Use com responsabilidade! 🛡️**
- ✅ **MacOS** (Opcional - Suportado)

### Versões Python
- Python 3.6+
- Testado em Python 3.8, 3.9, 3.10, 3.11

## Considerações de Segurança

⚠️ **Aviso Legal**: Esta ferramenta deve ser usada apenas em redes próprias ou com autorização explícita. O uso não autorizado pode violar leis locais.

### Boas Práticas
- Sempre obtenha autorização antes de escanear redes externas
- Use timeouts apropriados para evitar sobrecarga da rede
- Considere o impacto na rede durante varreduras extensivas
- Mantenha logs das atividades para auditoria

## Desenvolvimento

### Estrutura do Código
- **Classe PortScanner**: Lógica principal de varredura
- **Classe ScanResult**: Estrutura de dados para resultados
- **Funções auxiliares**: Expansão de CIDR, parsing de portas
- **Interface CLI**: Argumentos e formatação de saída

### Possíveis Melhorias Futuras
- Implementação de SYN Scan (raw sockets)
- Detecção de serviços por banner grabbing
- Interface gráfica (GUI)
- Suporte para IPv6
- Exportação em múltiplos formatos (JSON, XML)
- Profiles de varredura pré-configurados

## Troubleshooting

### Problemas Comuns

1. **"Permission denied" em UDP**
   - Solução: Execute com privilégios de administrador

2. **Muitos "filtered" results**
   - Solução: Ajuste o timeout `--timeout 10`

3. **Varredura muito lenta**
   - Solução: Reduza threads `--threads 50` ou aumente timeout

4. **"Connection refused" em todas as portas**
   - Solução: Verifique se o host está online e acessível

## Exemplo de Arquivo CSV de Saída

```csv
Host,Port,Protocol,Status
192.168.1.1,22,TCP,open
192.168.1.1,80,TCP,open
192.168.1.1,443,TCP,open
192.168.1.1,21,TCP,closed
192.168.1.1,25,TCP,filtered
```
