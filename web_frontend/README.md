# Interface Web do Scanner de Portas

## Como usar

### 1. Via Interface Web (Recomendado)

#### Iniciar o servidor Django:
```bash
cd web_frontend
python manage.py runserver
```

#### Acessar no navegador:
http://localhost:8000/

### 2. Via CLI (Linha de Comando)

Se a interface web não estiver disponível, use diretamente:

#### Exemplos básicos:
```bash
# Scan de porta específica
python port_scanner.py 192.168.1.1 --ports 80

# Scan de múltiplas portas
python port_scanner.py 192.168.1.1 --ports 22,80,443

# Scan de range de portas
python port_scanner.py 192.168.1.1 --ports 1-1000

# Scan de rede inteira
python port_scanner.py 192.168.1.0/24 --ports 22,80,443

# Scan UDP
python port_scanner.py 192.168.1.1 --ports 53,161 --protocol udp

# Scan TCP + UDP
python port_scanner.py 192.168.1.1 --ports 22,53,80,443 --protocol both
```

#### Opções avançadas:
```bash
# Com threads (mais rápido)
python port_scanner.py 192.168.1.0/24 --ports 1-1000 --threads 50

# Com timeout personalizado
python port_scanner.py 192.168.1.1 --ports 1-65535 --timeout 2

# Salvar em arquivo
python port_scanner.py 192.168.1.0/24 --ports 22,80,443 --output resultados.txt

# Formato JSON
python port_scanner.py 192.168.1.1 --ports 1-1000 --format json --output scan.json
```

## Recursos da Interface Web

- ✅ Formulário simples e intuitivo
- ✅ Validação de entrada
- ✅ Barra de progresso visual
- ✅ Resultados formatados por host
- ✅ Fallback para linha de comando
- ✅ Cópia automática de comandos CLI
- ✅ Design responsivo (funciona em celulares)

## Funcionalidades

### Targets suportados:

#### Formatos básicos:
- **IP único:** `192.168.1.1`
- **Hostname:** `google.com`
- **Range CIDR:** `192.168.1.0/24` (escaneia todos IPs da rede)

#### Múltiplos alvos (separados por vírgula):
- **Múltiplos IPs:** `192.168.1.1,192.168.1.10,192.168.1.20`
- **IPs + Hostnames:** `192.168.1.1,google.com,facebook.com`
- **Misto completo:** `127.0.0.1,192.168.1.0/28,google.com`

#### Exemplos práticos:
```bash
# Escanear 3 IPs específicos
192.168.1.1,192.168.1.10,192.168.1.50

# Escanear rede local + alguns sites
192.168.1.0/24,google.com,github.com

# Escanear localhost + gateway + DNS
127.0.0.1,192.168.1.1,8.8.8.8
```

### Portas:
- Porta única: `80`
- Múltiplas: `22,80,443`
- Range: `1-1000`
- Comuns: `1-65535`

### Protocolos:
- TCP (padrão)
- UDP  
- Ambos (TCP + UDP)

## Solução de Problemas

### Interface web não carrega:
1. Verifique se o Django está instalado: `pip install django`
2. Inicie o servidor: `python manage.py runserver`
3. Acesse: http://localhost:8000/

### Erro de backend:
- A interface mostrará automaticamente o comando CLI equivalente
- Copie e execute no terminal

### Scan muito lento:
- Use menos threads para redes estáveis
- Aumente o timeout para redes lentas
- Limite o range de portas
