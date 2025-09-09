# 🔍 Port Scanner - Ferramenta de Varredura TCP/UDP

Ferramenta completa de varredura de portas desenvolvida em Python com três interfaces distintas: Web, GUI e CLI.

## 🚀 Instalação e Execução Rápida

### 1. Instalação Automática
```bash
python quick_install.py
```

### 2. Executar Interface Web (Recomendada)
```bash
cd web_frontend
python manage.py runserver
```
🌐 **Acesse: http://localhost:8000**

### 3. Windows - Clique Duplo
- `start_web.bat` - Interface Web
- `start_gui.bat` - Interface GUI

## ✨ Características Principais

- ✅ **Varredura TCP/UDP** - Protocolos completos
- ✅ **Múltiplos alvos** - IP único, múltiplos IPs, CIDR, hostnames  
- ✅ **3 Interfaces** - Web moderna, GUI desktop, CLI para automação
- ✅ **Multi-threading** - Performance otimizada
- ✅ **Exportação** - JSON, TXT, CSV
- ✅ **Cross-platform** - Windows, Linux, macOS

## 📱 Interfaces Disponíveis

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
