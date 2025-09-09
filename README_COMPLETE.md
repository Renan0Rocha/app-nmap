# 🔍 Port Scanner - Ferramenta de Varredura de Portas TCP/UDP

Uma ferramenta completa de varredura de portas desenvolvida em Python, oferecendo múltiplas interfaces (CLI, GUI e Web) para escaneamento de redes TCP e UDP.

## 📋 Índice
- [Características](#características)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Interfaces Disponíveis](#interfaces-disponíveis)
- [Guia de Uso](#guia-de-uso)
- [Exemplos Práticos](#exemplos-práticos)
- [Configuração Avançada](#configuração-avançada)
- [Solução de Problemas](#solução-de-problemas)
- [Desenvolvimento](#desenvolvimento)

## ✨ Características

### 🎯 Funcionalidades Core
- ✅ **Varredura TCP/UDP**: Suporte completo para ambos protocolos
- ✅ **Múltiplos targets**: IP único, múltiplos IPs, ranges CIDR, hostnames
- ✅ **Detecção inteligente**: Identifica portas abertas, fechadas e filtradas
- ✅ **Multi-threading**: Escaneamento rápido com threads configuráveis
- ✅ **Timeout personalizável**: Adaptável para redes lentas/rápidas
- ✅ **Exportação de resultados**: JSON, TXT e CSV

### 🖥️ Interfaces Disponíveis
1. **🖱️ Interface Web** (Recomendada) - Interface moderna e intuitiva
2. **🖼️ Interface GUI** - Aplicação desktop com Tkinter
3. **⌨️ Interface CLI** - Linha de comando para automação

### 🎮 Alvos Suportados
- **IP único**: `192.168.1.1`
- **Múltiplos IPs**: `192.168.1.1,192.168.1.10,192.168.1.20`
- **Range CIDR**: `192.168.1.0/24` (rede completa)
- **Hostnames**: `google.com,github.com`
- **Misto**: `127.0.0.1,192.168.1.0/28,google.com`

## 🔧 Pré-requisitos

### Sistema Operacional
- ✅ Windows 10/11
- ✅ Linux (Ubuntu 18.04+)
- ✅ macOS 10.15+

### Software Necessário
- **Python 3.8+** (Recomendado: Python 3.11)
- **pip** (gerenciador de pacotes Python)

### Verificar instalação:
```bash
python --version
pip --version
```

## 📦 Instalação

### Opção 1: Instalação Automática (Recomendada)
```bash
# Clone o repositório
git clone https://github.com/user/port-scanner.git
cd port-scanner

# Execute o instalador automático
python install.py
```

### Opção 2: Instalação Manual

#### 1. Dependências principais
```bash
pip install -r requirements.txt
```

#### 2. Para interface web (opcional)
```bash
cd web_frontend
pip install -r requirements_web.txt
```

#### 3. Para interface GUI (opcional)
```bash
# Tkinter já vem com Python, mas em alguns Linux:
sudo apt-get install python3-tk  # Ubuntu/Debian
```

## 🚀 Interfaces Disponíveis

## 1. 🌐 Interface Web (Recomendada)

### Iniciar servidor:
```bash
cd web_frontend
python manage.py runserver
```

### Acessar:
🌐 **http://localhost:8000**

### Características:
- ✅ Interface moderna e responsiva
- ✅ Formulários intuitivos
- ✅ Resultados em tempo real
- ✅ Exportação de dados
- ✅ Histórico de scans
- ✅ Suporte a dispositivos móveis

---

## 2. 🖼️ Interface GUI Desktop

### Executar:
```bash
# Opção 1: Python
python gui_scanner.py

# Opção 2: Arquivo batch (Windows)
run_gui.bat
```

### Características:
- ✅ Interface gráfica nativa
- ✅ Configuração visual
- ✅ Barras de progresso
- ✅ Salvar/carregar configurações

---

## 3. ⌨️ Interface CLI (Linha de Comando)

### Uso básico:
```bash
python port_scanner.py TARGET --ports PORTAS [opções]
```

### Exemplos CLI:
```bash
# Scan básico
python port_scanner.py 192.168.1.1 --ports 80,443

# Scan de rede completa
python port_scanner.py 192.168.1.0/24 --ports common

# Scan UDP
python port_scanner.py 192.168.1.1 --ports 53,161 --protocol udp

# Scan TCP + UDP
python port_scanner.py 192.168.1.1 --ports 22,53,80 --protocol both

# Alta performance
python port_scanner.py 192.168.1.0/24 --ports 1-1000 --threads 100 --timeout 1

# Salvar resultados
python port_scanner.py 192.168.1.1 --ports 1-65535 --output resultados.json --format json
```

## 📚 Guia de Uso

### 🎯 Definindo Targets

#### Formatos suportados:
```bash
# IP único
192.168.1.1

# Múltiplos IPs (separados por vírgula)
192.168.1.1,192.168.1.10,192.168.1.20

# Range CIDR (rede completa)
192.168.1.0/24        # 254 IPs
10.0.0.0/16          # 65,534 IPs
192.168.1.0/28       # 14 IPs

# Hostnames
google.com
github.com,stackoverflow.com

# Combinado (IPs + hostnames + CIDR)
127.0.0.1,192.168.1.0/28,google.com,github.com
```

### 🔌 Definindo Portas

#### Formatos de portas:
```bash
# Porta única
80

# Múltiplas portas
80,443,22,8080

# Range de portas
1-1000
80-90

# Portas comuns (predefinidas)
common              # 21,22,23,25,53,80,110,443,993,995

# Combinado
22,80-90,443,8000-8080
```

### ⚙️ Opções Avançadas

#### Parâmetros de performance:
```bash
--threads 50         # Número de threads (padrão: 50)
--timeout 3          # Timeout por porta em segundos (padrão: 3)
--protocol tcp       # tcp, udp ou both (padrão: tcp)
```

#### Saída e formatação:
```bash
--output arquivo.txt    # Salvar resultados
--format json          # json, txt, csv (padrão: txt)
--verbose              # Saída detalhada
--quiet               # Saída mínima
```

## 🎯 Exemplos Práticos

### Cenário 1: Auditoria de Rede Local
```bash
# Escanear toda a rede local em busca de serviços comuns
python port_scanner.py 192.168.1.0/24 --ports common --threads 100 --output rede_local.json --format json
```

### Cenário 2: Verificação de Servidor Web
```bash
# Verificar portas web e SSH em servidor específico
python port_scanner.py 192.168.1.100 --ports 22,80,443,8080,8443 --timeout 5
```

### Cenário 3: Descoberta de Serviços UDP
```bash
# Buscar serviços UDP comuns
python port_scanner.py 192.168.1.1 --ports 53,161,162,123,69 --protocol udp
```

### Cenário 4: Scan Completo de Segurança
```bash
# Scan completo TCP + UDP (cuidado: pode ser lento)
python port_scanner.py 192.168.1.100 --ports 1-65535 --protocol both --threads 200 --timeout 1 --output scan_completo.csv --format csv
```

### Cenário 5: Múltiplos Alvos
```bash
# Escanear múltiplos servidores importantes
python port_scanner.py 192.168.1.1,192.168.1.100,google.com --ports 22,80,443 --output servidores.txt
```

## ⚙️ Configuração Avançada

### Arquivo de configuração (config.py):
```python
# Configurações padrão
DEFAULT_TIMEOUT = 3
DEFAULT_THREADS = 50
DEFAULT_PORTS = "common"
DEFAULT_PROTOCOL = "tcp"

# Portas comuns predefinidas
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 8080]

# Configurações de performance
MAX_THREADS = 500
MIN_TIMEOUT = 0.1
MAX_TIMEOUT = 60
```

### Personalizar portas comuns:
```python
# Editar config.py
COMMON_PORTS = [22, 80, 443, 3389, 5432, 3306, 1433, 5984]
```

## 🔧 Solução de Problemas

### ❌ Problemas Comuns

#### 1. "Comando não encontrado" ou "ModuleNotFoundError"
```bash
# Verificar Python
python --version

# Instalar dependências
pip install -r requirements.txt

# Para interface web
cd web_frontend
pip install -r requirements_web.txt
```

#### 2. Interface web não carrega
```bash
# Verificar se Django está instalado
pip install django

# Iniciar servidor na porta correta
python manage.py runserver 8000

# Acessar: http://localhost:8000
```

#### 3. Scan muito lento
```bash
# Aumentar threads e diminuir timeout
python port_scanner.py TARGET --threads 100 --timeout 1

# Para redes locais, use timeout baixo
--timeout 0.5

# Para redes externas, use timeout maior
--timeout 5
```

#### 4. "Permission denied" (Linux/macOS)
```bash
# Usar sudo para portas privilegiadas ou raw sockets
sudo python port_scanner.py TARGET --ports 1-1024

# Ou usar portas não privilegiadas
python port_scanner.py TARGET --ports 1024-65535
```

#### 5. Firewall bloqueando scans
```bash
# Em redes corporativas, alguns scans podem ser bloqueados
# Use timeouts maiores e menos threads
python port_scanner.py TARGET --timeout 10 --threads 10
```

### 🐛 Logs e Debug

#### Habilitar modo verbose:
```bash
python port_scanner.py TARGET --ports PORTAS --verbose
```

#### Interface web - logs Django:
```bash
# Ver logs do servidor
cd web_frontend
python manage.py runserver --verbosity 2
```

## 👨‍💻 Desenvolvimento

### Estrutura do projeto:
```
app-nmap/
├── 📄 port_scanner.py          # Engine principal
├── 📄 gui_scanner.py           # Interface GUI
├── 📄 config.py               # Configurações
├── 📄 test_scanner.py         # Testes unitários
├── 📄 requirements.txt        # Dependências principais
├── 🗂️ web_frontend/           # Interface web Django
│   ├── 📄 manage.py
│   ├── 📄 requirements_web.txt
│   ├── 🗂️ portscanner_web/   # Configurações Django
│   ├── 🗂️ scanner/           # App Django
│   └── 🗂️ templates/         # Templates HTML
└── 🗂️ __pycache__/           # Cache Python
```

### Executar testes:
```bash
python test_scanner.py
```

### Contribuir:
1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Add: nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## ⚖️ Considerações Legais

### ⚠️ **AVISO IMPORTANTE**
Esta ferramenta deve ser usada apenas em:
- ✅ Redes próprias
- ✅ Sistemas com autorização explícita
- ✅ Ambientes de teste/laboratório
- ✅ Auditorias autorizadas

### 🚫 **NÃO USE PARA**
- ❌ Redes de terceiros sem permissão
- ❌ Atividades maliciosas
- ❌ Violação de termos de serviço
- ❌ Atividades ilegais

**O uso inadequado pode violar leis locais e internacionais. Use com responsabilidade.**

## 📞 Suporte

### 🆘 Precisa de ajuda?
1. Verifique a [Solução de Problemas](#solução-de-problemas)
2. Execute testes: `python test_scanner.py`
3. Verifique logs: `--verbose`
4. Abra uma issue no GitHub

### 📈 Performance
- **Rede local**: Use `--timeout 1 --threads 100`
- **Rede externa**: Use `--timeout 5 --threads 50`
- **Scan completo**: Use `--timeout 2 --threads 200`

---

**Desenvolvido para fins educacionais e de segurança. Use com responsabilidade! 🛡️**
