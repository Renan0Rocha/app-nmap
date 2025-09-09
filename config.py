# Configuração da Ferramenta de Varredura de Portas

# Este arquivo contém configurações padrão e perfis de varredura

# Configurações Gerais
DEFAULT_TIMEOUT = 3
DEFAULT_THREADS = 100
DEFAULT_PROTOCOL = "TCP"

# Perfis de Varredura
SCAN_PROFILES = {
    "quick": {
        "description": "Varredura rápida - portas mais comuns",
        "ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 8080],
        "timeout": 1,
        "threads": 200,
        "protocols": ["TCP"]
    },
    
    "common": {
        "description": "Varredura padrão - portas comuns de serviços",
        "ports": [20, 21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 
                 445, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443],
        "timeout": 3,
        "threads": 100,
        "protocols": ["TCP"]
    },
    
    "comprehensive": {
        "description": "Varredura completa - top 1000 portas",
        "ports": list(range(1, 1001)),
        "timeout": 5,
        "threads": 50,
        "protocols": ["TCP"]
    },
    
    "stealth": {
        "description": "Varredura stealth - lenta e discreta",
        "ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995],
        "timeout": 10,
        "threads": 5,
        "protocols": ["TCP"]
    },
    
    "dns": {
        "description": "Varredura focada em DNS",
        "ports": [53],
        "timeout": 2,
        "threads": 10,
        "protocols": ["TCP", "UDP"]
    },
    
    "web": {
        "description": "Varredura focada em serviços web",
        "ports": [80, 443, 8080, 8443, 8000, 8888, 9000, 9090],
        "timeout": 3,
        "threads": 50,
        "protocols": ["TCP"]
    },
    
    "database": {
        "description": "Varredura focada em bancos de dados",
        "ports": [1433, 1521, 3306, 5432, 6379, 27017],
        "timeout": 5,
        "threads": 20,
        "protocols": ["TCP"]
    },
    
    "mail": {
        "description": "Varredura focada em serviços de email",
        "ports": [25, 110, 143, 465, 587, 993, 995],
        "timeout": 5,
        "threads": 30,
        "protocols": ["TCP"]
    }
}

# Portas por Categorias de Serviços
SERVICE_PORTS = {
    "web": [80, 443, 8080, 8443, 8000, 8888, 9000, 9090, 3000, 5000],
    "ssh": [22],
    "ftp": [20, 21],
    "mail": [25, 110, 143, 465, 587, 993, 995],
    "dns": [53],
    "dhcp": [67, 68],
    "http_alt": [8080, 8443, 8000, 8888, 9000, 9090],
    "database": [1433, 1521, 3306, 5432, 6379, 27017, 28017],
    "remote": [22, 23, 3389, 5900, 5901, 5902],
    "file_sharing": [135, 139, 445, 2049],
    "voip": [5060, 5061],
    "gaming": [25565, 7777, 27015],
    "monitoring": [161, 162, 10050, 12489],
    "backup": [10000, 10001, 10002],
    "virtualization": [902, 903, 8006, 8007]
}

# Configurações de Timeout por Tipo de Rede
NETWORK_TIMEOUTS = {
    "local": 1,      # Rede local (192.168.x.x, 10.x.x.x)
    "wan": 5,        # Rede externa
    "slow": 10       # Redes lentas ou com alta latência
}

# Configurações de Threads por Tipo de Varredura
THREAD_CONFIGS = {
    "aggressive": 500,   # Varredura agressiva
    "normal": 100,       # Varredura normal
    "conservative": 50,  # Varredura conservadora
    "stealth": 10        # Varredura stealth
}

# Mensagens de Status Personalizadas
STATUS_MESSAGES = {
    "open": "🟢 ABERTA",
    "closed": "🔴 FECHADA", 
    "filtered": "🟡 FILTRADA",
    "open|filtered": "🟠 ABERTA|FILTRADA"
}

# Configurações de Saída
OUTPUT_FORMATS = {
    "csv": {
        "extension": ".csv",
        "headers": ["Host", "Port", "Protocol", "Status", "Timestamp"]
    },
    "json": {
        "extension": ".json", 
        "format": "structured"
    },
    "xml": {
        "extension": ".xml",
        "format": "structured"
    },
    "txt": {
        "extension": ".txt",
        "format": "human_readable"
    }
}

# Configurações de Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "file": "port_scanner.log"
}

# Lista de IPs Privados (RFC 1918)
PRIVATE_IP_RANGES = [
    "10.0.0.0/8",
    "172.16.0.0/12", 
    "192.168.0.0/16",
    "127.0.0.0/8"
]

# Configurações de Rate Limiting
RATE_LIMITING = {
    "max_requests_per_second": 100,
    "burst_size": 200,
    "delay_between_hosts": 0.1
}

# Configurações de User-Agent para HTTP Detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

# Payloads para Detecção UDP
UDP_PAYLOADS = {
    53: b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01',  # DNS query
    123: b'\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # NTP
    161: b'\x30\x26\x02\x01\x00\x04\x06\x70\x75\x62\x6c\x69\x63\xa0\x19\x02\x04\x00\x00\x00\x00\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00',  # SNMP
    "default": b"PORT_SCAN_TEST_PACKET"
}
