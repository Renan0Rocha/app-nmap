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

## Técnicas Implementadas

### TCP Scanning
- **Método**: Connect Scan (TCP Three-way Handshake)
- **Funcionamento**: Tenta estabelecer conexão TCP completa
- **Vantagens**: Simples, confiável, não requer privilégios especiais
- **Detecção**: 
  - OPEN: Conexão estabelecida com sucesso
  - CLOSED: Conexão recusada (RST packet)
  - FILTERED: Timeout (firewall/filtros)



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








