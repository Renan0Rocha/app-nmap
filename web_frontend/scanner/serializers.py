from rest_framework import serializers
from .models import ScanJob, ScanResult, ScanHistory


class ScanJobSerializer(serializers.ModelSerializer):
    """Serializer para jobs de varredura"""
    
    class Meta:
        model = ScanJob
        fields = [
            'id', 'target', 'ports', 'protocols', 'timeout', 'threads',
            'status', 'created_at', 'started_at', 'completed_at',
            'progress', 'total_ports', 'scanned_ports', 'error_message'
        ]
        read_only_fields = [
            'id', 'status', 'created_at', 'started_at', 'completed_at',
            'progress', 'total_ports', 'scanned_ports', 'error_message'
        ]

    def validate_target(self, value):
        """Valida o campo target"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Target não pode estar vazio")
        return value.strip()

    def validate_ports(self, value):
        """Valida o campo ports"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Portas não podem estar vazias")
        return value.strip()

    def validate_timeout(self, value):
        """Valida timeout"""
        if value < 1 or value > 60:
            raise serializers.ValidationError("Timeout deve ser entre 1 e 60 segundos")
        return value

    def validate_threads(self, value):
        """Valida número de threads"""
        if value < 1 or value > 500:
            raise serializers.ValidationError("Threads deve ser entre 1 e 500")
        return value


class ScanResultSerializer(serializers.ModelSerializer):
    """Serializer para resultados da varredura"""
    
    class Meta:
        model = ScanResult
        fields = [
            'id', 'host', 'port', 'protocol', 'status',
            'response_time', 'created_at'
        ]


class ScanHistorySerializer(serializers.ModelSerializer):
    """Serializer para histórico de varreduras"""
    
    job = ScanJobSerializer(read_only=True)
    
    class Meta:
        model = ScanHistory
        fields = [
            'id', 'job', 'summary', 'execution_time',
            'open_ports', 'closed_ports', 'filtered_ports',
            'hosts_scanned', 'hosts_active'
        ]


class ScanJobCreateSerializer(serializers.Serializer):
    """Serializer simplificado para criar jobs"""
    
    target = serializers.CharField(max_length=500)
    ports = serializers.CharField(max_length=500, required=False, default="80,443")
    use_common_ports = serializers.BooleanField(default=False)
    use_top100 = serializers.BooleanField(default=False)
    use_top1000 = serializers.BooleanField(default=False)
    
    tcp = serializers.BooleanField(default=True)
    udp = serializers.BooleanField(default=False)
    
    timeout = serializers.IntegerField(default=3, min_value=1, max_value=60)
    threads = serializers.IntegerField(default=50, min_value=1, max_value=500)
    
    def validate(self, data):
        """Validação geral"""
        if not data.get('tcp') and not data.get('udp'):
            raise serializers.ValidationError("Selecione pelo menos um protocolo (TCP ou UDP)")
        
        # Se nenhuma opção de porta especial foi selecionada, deve ter portas customizadas
        if not data.get('use_common_ports') and not data.get('use_top100') and not data.get('use_top1000'):
            if not data.get('ports') or len(data.get('ports', '').strip()) == 0:
                raise serializers.ValidationError("Especifique portas ou selecione uma opção de portas predefinidas")
        
        return data


class ScanStatusSerializer(serializers.Serializer):
    """Serializer para status da varredura em tempo real"""
    
    job_id = serializers.UUIDField()
    status = serializers.CharField()
    progress = serializers.IntegerField()
    scanned_ports = serializers.IntegerField()
    total_ports = serializers.IntegerField()
    current_host = serializers.CharField(required=False)
    estimated_time_remaining = serializers.IntegerField(required=False)
    results_count = serializers.IntegerField(default=0)
