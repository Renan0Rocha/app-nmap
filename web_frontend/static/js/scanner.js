/**
 * Port Scanner Web Interface - JavaScript Controller
 * Gerencia todas as interações da interface web
 */

class PortScannerApp {
    constructor() {
        this.csrfToken = this.getCSRFToken();
        this.currentJobId = null;
        this.progressInterval = null;
        
        this.initializeEventListeners();
        this.loadDashboardData();
        this.loadRecentJobs();
        
        // Auto-refresh dashboard a cada 30 segundos
        setInterval(() => {
            this.loadDashboardData();
            this.loadRecentJobs();
        }, 30000);
    }

    /**
     * Obtém o token CSRF do Django
     */
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    }

    /**
     * Inicializa todos os event listeners
     */
    initializeEventListeners() {
        // Quick Scan Form
        document.getElementById('quickScanForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleQuickScan();
        });

        // Advanced Scan Form
        document.getElementById('advancedScanForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleAdvancedScan();
        });

        // Port Option Changes
        document.querySelectorAll('input[name="portOption"]').forEach(radio => {
            radio.addEventListener('change', this.handlePortOptionChange.bind(this));
        });

        // Stop Scan Button
        document.getElementById('stopScanBtn')?.addEventListener('click', () => {
            this.stopCurrentScan();
        });

        // View Results Button
        document.getElementById('viewResultsBtn')?.addEventListener('click', () => {
            this.viewScanResults();
        });

        // Help Modal Trigger
        document.querySelector('[data-bs-target="#helpModal"]')?.addEventListener('click', () => {
            // Carrega conteúdo de ajuda se necessário
        });
    }

    /**
     * Manipula mudança nas opções de porta
     */
    handlePortOptionChange(event) {
        const customPortsInput = document.getElementById('customPortsInput');
        const portsInput = document.getElementById('portsInput');
        
        if (event.target.value === 'custom') {
            customPortsInput.style.display = 'block';
            portsInput.required = true;
            portsInput.value = '';
            portsInput.placeholder = '80,443,8080 ou 1-1000 ou 80,90-95,443';
        } else {
            customPortsInput.style.display = 'none';
            portsInput.required = false;
            
            // Define valores padrão baseado na seleção
            switch (event.target.value) {
                case 'common':
                    portsInput.value = 'common';
                    break;
                case 'top100':
                    portsInput.value = 'top100';
                    break;
                case 'top1000':
                    portsInput.value = 'top1000';
                    break;
            }
        }
    }

    /**
     * Executa scan rápido
     */
    async handleQuickScan() {
        const target = document.getElementById('quickTarget').value.trim();
        
        if (!target) {
            this.showAlert('Por favor, insira um target válido.', 'warning');
            return;
        }

        const scanData = {
            target: target,
            ports: 'common',
            protocols: ['tcp'],
            timeout: 3,
            threads: 50
        };

        await this.startScan(scanData);
    }

    /**
     * Executa scan avançado
     */
    async handleAdvancedScan() {
        const target = document.getElementById('advancedTarget').value.trim();
        
        if (!target) {
            this.showAlert('Por favor, insira um target válido.', 'warning');
            return;
        }

        // Coleta configurações de porta
        const portOption = document.querySelector('input[name="portOption"]:checked').value;
        let ports;
        
        if (portOption === 'custom') {
            ports = document.getElementById('portsInput').value.trim();
            if (!ports) {
                this.showAlert('Por favor, especifique as portas a serem escaneadas.', 'warning');
                return;
            }
        } else {
            ports = portOption;
        }

        // Coleta protocolos
        const protocols = [];
        if (document.getElementById('tcpProtocol').checked) protocols.push('tcp');
        if (document.getElementById('udpProtocol').checked) protocols.push('udp');
        
        if (protocols.length === 0) {
            this.showAlert('Selecione pelo menos um protocolo.', 'warning');
            return;
        }

        const scanData = {
            target: target,
            ports: ports,
            protocols: protocols,
            timeout: parseInt(document.getElementById('timeoutSetting').value),
            threads: parseInt(document.getElementById('threadsSetting').value)
        };

        // Fecha modal de configuração e inicia scan
        const modal = bootstrap.Modal.getInstance(document.getElementById('newScanModal'));
        modal.hide();
        
        await this.startScan(scanData);
    }

    /**
     * Inicia uma nova varredura
     */
    async startScan(scanData) {
        try {
            this.showProgressModal();
            
            const response = await fetch('/api/scans/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify(scanData)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Erro ao iniciar varredura');
            }

            this.currentJobId = result.job_id;
            this.updateProgressInfo(scanData.target, 'Iniciando varredura...');
            this.startProgressPolling();

        } catch (error) {
            console.error('Erro ao iniciar scan:', error);
            this.hideProgressModal();
            this.showAlert(`Erro ao iniciar varredura: ${error.message}`, 'danger');
        }
    }

    /**
     * Para a varredura atual
     */
    async stopCurrentScan() {
        if (!this.currentJobId) return;

        try {
            const response = await fetch(`/api/scans/${this.currentJobId}/stop/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken
                }
            });

            if (response.ok) {
                this.stopProgressPolling();
                this.hideProgressModal();
                this.showAlert('Varredura interrompida pelo usuário.', 'info');
            }
        } catch (error) {
            console.error('Erro ao parar scan:', error);
            this.showAlert('Erro ao interromper varredura.', 'danger');
        }
    }

    /**
     * Mostra o modal de progresso
     */
    showProgressModal() {
        const modal = new bootstrap.Modal(document.getElementById('progressModal'));
        modal.show();
        
        // Reset progress
        this.updateProgress(0, 0, 0, 0);
    }

    /**
     * Esconde o modal de progresso
     */
    hideProgressModal() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('progressModal'));
        if (modal) {
            modal.hide();
        }
    }

    /**
     * Atualiza informações do progresso
     */
    updateProgressInfo(target, status) {
        document.getElementById('progressTarget').textContent = `Target: ${target}`;
        document.getElementById('progressStatus').textContent = status;
    }

    /**
     * Atualiza barra de progresso
     */
    updateProgress(scanned, total, open, percentage) {
        document.getElementById('scannedCount').textContent = scanned;
        document.getElementById('totalCount').textContent = total;
        document.getElementById('openCount').textContent = open;
        
        const progressBar = document.getElementById('progressBar');
        progressBar.style.width = `${percentage}%`;
        progressBar.textContent = `${Math.round(percentage)}%`;
    }

    /**
     * Inicia polling do progresso
     */
    startProgressPolling() {
        this.progressInterval = setInterval(async () => {
            await this.checkProgress();
        }, 2000);
    }

    /**
     * Para polling do progresso
     */
    stopProgressPolling() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }

    /**
     * Verifica progresso da varredura
     */
    async checkProgress() {
        if (!this.currentJobId) return;

        try {
            const response = await fetch(`/api/scans/${this.currentJobId}/progress/`);
            const progress = await response.json();

            if (!response.ok) {
                throw new Error('Erro ao verificar progresso');
            }

            // Atualiza interface
            this.updateProgress(
                progress.scanned || 0,
                progress.total || 0,
                progress.open || 0,
                progress.percentage || 0
            );

            // Atualiza status
            let statusText = 'Escaneando...';
            if (progress.status === 'completed') {
                statusText = 'Varredura concluída!';
                this.stopProgressPolling();
                this.showCompleteButton();
            } else if (progress.status === 'failed') {
                statusText = 'Varredura falhada!';
                this.stopProgressPolling();
                this.showAlert('A varredura falhou. Verifique os logs.', 'danger');
            }

            document.getElementById('progressStatus').textContent = statusText;

        } catch (error) {
            console.error('Erro ao verificar progresso:', error);
            this.stopProgressPolling();
        }
    }

    /**
     * Mostra botão de visualizar resultados
     */
    showCompleteButton() {
        document.getElementById('stopScanBtn').classList.add('d-none');
        document.getElementById('viewResultsBtn').classList.remove('d-none');
    }

    /**
     * Visualiza resultados da varredura
     */
    viewScanResults() {
        this.hideProgressModal();
        window.location.href = `/results/${this.currentJobId}/`;
    }

    /**
     * Carrega dados do dashboard
     */
    async loadDashboardData() {
        try {
            const response = await fetch('/api/dashboard/stats/');
            const stats = await response.json();

            if (response.ok) {
                this.updateDashboardStats(stats);
            }
        } catch (error) {
            console.error('Erro ao carregar stats do dashboard:', error);
        }
    }

    /**
     * Atualiza estatísticas do dashboard
     */
    updateDashboardStats(stats) {
        const elements = {
            'totalScans': stats.total_scans || 0,
            'activeScans': stats.active_scans || 0,
            'hostsFound': stats.hosts_found || 0,
            'openPorts': stats.open_ports || 0
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                this.animateCounter(element, parseInt(element.textContent) || 0, value);
            }
        });
    }

    /**
     * Anima contador numérico
     */
    animateCounter(element, start, end) {
        const duration = 1000;
        const range = end - start;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.floor(start + (range * progress));
            element.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    /**
     * Carrega trabalhos recentes
     */
    async loadRecentJobs() {
        try {
            const response = await fetch('/api/scans/?limit=5');
            const jobs = await response.json();

            if (response.ok && jobs.results) {
                this.updateRecentJobs(jobs.results);
            }
        } catch (error) {
            console.error('Erro ao carregar jobs recentes:', error);
        }
    }

    /**
     * Atualiza lista de jobs recentes
     */
    updateRecentJobs(jobs) {
        const container = document.getElementById('recentJobs');
        if (!container) return;

        if (jobs.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                    <p class="text-muted">Nenhuma varredura encontrada</p>
                </div>
            `;
            return;
        }

        container.innerHTML = jobs.map(job => `
            <div class="job-item">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="mb-1">${job.target}</h6>
                        <p class="mb-1 text-muted">${job.ports} | ${job.protocols.join(', ').toUpperCase()}</p>
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>
                            ${this.formatDateTime(job.created_at)}
                        </small>
                    </div>
                    <div class="text-end">
                        <span class="job-status ${job.status}">${this.formatStatus(job.status)}</span>
                        ${job.status === 'completed' ? 
                            `<div class="mt-1"><a href="/results/${job.id}/" class="btn btn-sm btn-outline-primary">Ver Resultados</a></div>` : ''}
                    </div>
                </div>
            </div>
        `).join('');
    }

    /**
     * Formata status do job
     */
    formatStatus(status) {
        const statusMap = {
            'pending': 'Pendente',
            'running': 'Executando',
            'completed': 'Concluído',
            'failed': 'Falhou'
        };
        return statusMap[status] || status;
    }

    /**
     * Formata data e hora
     */
    formatDateTime(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;
        
        // Se foi há menos de 1 hora, mostra tempo relativo
        if (diff < 3600000) {
            const minutes = Math.floor(diff / 60000);
            return minutes <= 1 ? 'Agora há pouco' : `${minutes}min atrás`;
        }
        
        // Se foi hoje, mostra hora
        if (date.toDateString() === now.toDateString()) {
            return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
        }
        
        // Senão, mostra data
        return date.toLocaleDateString('pt-BR');
    }

    /**
     * Mostra alerta
     */
    showAlert(message, type = 'info') {
        // Remove alertas existentes
        document.querySelectorAll('.alert-dismissible').forEach(alert => alert.remove());

        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        // Adiciona no topo do conteúdo principal
        const container = document.querySelector('.container-fluid');
        if (container) {
            container.insertAdjacentHTML('afterbegin', alertHtml);
            
            // Auto-remove após 5 segundos
            setTimeout(() => {
                const alert = container.querySelector('.alert-dismissible');
                if (alert) {
                    alert.remove();
                }
            }, 5000);
        }
    }

    /**
     * Retorna ícone do alerta baseado no tipo
     */
    getAlertIcon(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    new PortScannerApp();
});

// Utilitários globais
window.PortScannerUtils = {
    /**
     * Copia texto para clipboard
     */
    copyToClipboard: async function(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            // Fallback para navegadores mais antigos
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return true;
        }
    },

    /**
     * Formata duração em segundos para texto legível
     */
    formatDuration: function(seconds) {
        if (seconds < 60) return `${seconds}s`;
        if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours}h ${minutes}m`;
    },

    /**
     * Valida formato de IP
     */
    isValidIP: function(ip) {
        const ipv4Regex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        return ipv4Regex.test(ip);
    },

    /**
     * Valida formato CIDR
     */
    isValidCIDR: function(cidr) {
        const cidrRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/([0-9]|[1-2][0-9]|3[0-2])$/;
        return cidrRegex.test(cidr);
    }
};
