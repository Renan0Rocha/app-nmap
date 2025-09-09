#!/usr/bin/env python3
"""
Interface Gráfica para a Ferramenta de Varredura de Portas
Implementação opcional usando tkinter (incluso no Python padrão)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import time
from port_scanner import PortScanner, expand_cidr, expand_port_range, get_common_ports


class PortScannerGUI:
    """Interface gráfica para o scanner de portas"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Ferramenta de Varredura de Portas")
        self.root.geometry("800x700")
        
        # Queue para comunicação entre threads
        self.result_queue = queue.Queue()
        
        # Variáveis
        self.scanning = False
        self.scan_thread = None
        
        self.setup_ui()
        
        # Inicia verificação da queue
        self.root.after(100, self.check_queue)
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurações de target
        target_frame = ttk.LabelFrame(main_frame, text="Configurações de Target", padding="5")
        target_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(target_frame, text="Target (IP/CIDR/hostname):").grid(row=0, column=0, sticky=tk.W)
        self.target_var = tk.StringVar(value="127.0.0.1")
        target_entry = ttk.Entry(target_frame, textvariable=self.target_var, width=40)
        target_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Configurações de portas
        ports_frame = ttk.LabelFrame(main_frame, text="Configurações de Portas", padding="5")
        ports_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Opções de portas
        self.port_mode = tk.StringVar(value="custom")
        
        ttk.Radiobutton(ports_frame, text="Portas personalizadas:", 
                       variable=self.port_mode, value="custom").grid(row=0, column=0, sticky=tk.W)
        self.custom_ports_var = tk.StringVar(value="22,80,443")
        custom_entry = ttk.Entry(ports_frame, textvariable=self.custom_ports_var, width=30)
        custom_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        ttk.Radiobutton(ports_frame, text="Portas comuns", 
                       variable=self.port_mode, value="common").grid(row=1, column=0, sticky=tk.W)
        
        ttk.Radiobutton(ports_frame, text="Top 100 portas", 
                       variable=self.port_mode, value="top100").grid(row=2, column=0, sticky=tk.W)
        
        ttk.Radiobutton(ports_frame, text="Top 1000 portas", 
                       variable=self.port_mode, value="top1000").grid(row=3, column=0, sticky=tk.W)
        
        # Configurações de protocolo
        protocol_frame = ttk.LabelFrame(main_frame, text="Protocolos", padding="5")
        protocol_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.tcp_var = tk.BooleanVar(value=True)
        self.udp_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(protocol_frame, text="TCP", variable=self.tcp_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(protocol_frame, text="UDP", variable=self.udp_var).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Configurações avançadas
        advanced_frame = ttk.LabelFrame(main_frame, text="Configurações Avançadas", padding="5")
        advanced_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(advanced_frame, text="Timeout (s):").grid(row=0, column=0, sticky=tk.W)
        self.timeout_var = tk.StringVar(value="3")
        timeout_spin = ttk.Spinbox(advanced_frame, from_=1, to=30, width=10, textvariable=self.timeout_var)
        timeout_spin.grid(row=0, column=1, sticky=tk.W, padx=(5, 20))
        
        ttk.Label(advanced_frame, text="Threads:").grid(row=0, column=2, sticky=tk.W)
        self.threads_var = tk.StringVar(value="100")
        threads_spin = ttk.Spinbox(advanced_frame, from_=1, to=500, width=10, textvariable=self.threads_var)
        threads_spin.grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        # Botões de controle
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.scan_button = ttk.Button(control_frame, text="Iniciar Varredura", command=self.start_scan)
        self.scan_button.grid(row=0, column=0, padx=(0, 5))
        
        self.stop_button = ttk.Button(control_frame, text="Parar", command=self.stop_scan, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 5))
        
        ttk.Button(control_frame, text="Salvar Resultados", command=self.save_results).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(control_frame, text="Limpar", command=self.clear_results).grid(row=0, column=3)
        
        # Barra de progresso
        self.progress_var = tk.StringVar(value="Pronto para iniciar varredura")
        ttk.Label(main_frame, textvariable=self.progress_var).grid(row=5, column=0, columnspan=2, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 10))
        
        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="5")
        results_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Treeview para resultados
        columns = ("Host", "Port", "Protocol", "Status")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar redimensionamento
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        target_frame.columnconfigure(1, weight=1)
        ports_frame.columnconfigure(1, weight=1)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Variável para armazenar resultados
        self.scan_results = []
    
    def start_scan(self):
        """Inicia a varredura"""
        if self.scanning:
            return
        
        # Valida entrada
        target = self.target_var.get().strip()
        if not target:
            messagebox.showerror("Erro", "Por favor, especifique um target")
            return
        
        if not self.tcp_var.get() and not self.udp_var.get():
            messagebox.showerror("Erro", "Selecione pelo menos um protocolo (TCP ou UDP)")
            return
        
        # Prepara configurações
        try:
            timeout = float(self.timeout_var.get())
            threads = int(self.threads_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Timeout e threads devem ser números válidos")
            return
        
        # Determina portas
        ports = []
        port_mode = self.port_mode.get()
        
        if port_mode == "custom":
            custom_ports = self.custom_ports_var.get().strip()
            if not custom_ports:
                messagebox.showerror("Erro", "Especifique portas personalizadas ou selecione outra opção")
                return
            try:
                ports = expand_port_range(custom_ports)
            except ValueError:
                messagebox.showerror("Erro", "Formato de portas inválido")
                return
        else:
            common_ports = get_common_ports()
            if port_mode == "common":
                if self.tcp_var.get():
                    ports.extend(common_ports['tcp_common'])
                if self.udp_var.get():
                    ports.extend(common_ports['udp_common'])
            elif port_mode == "top100":
                ports.extend(common_ports['tcp_top100'])
            elif port_mode == "top1000":
                ports.extend(common_ports['tcp_top1000'])
        
        ports = sorted(list(set(ports)))
        
        # Determina protocolos
        protocols = []
        if self.tcp_var.get():
            protocols.append('TCP')
        if self.udp_var.get():
            protocols.append('UDP')
        
        # Expande targets
        try:
            targets = expand_cidr(target)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar target: {e}")
            return
        
        # Configura UI para varredura
        self.scanning = True
        self.scan_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.progress_bar.start()
        self.clear_results()
        
        # Inicia thread de varredura
        self.scan_thread = threading.Thread(
            target=self.scan_worker,
            args=(targets, ports, protocols, timeout, threads),
            daemon=True
        )
        self.scan_thread.start()
    
    def scan_worker(self, targets, ports, protocols, timeout, threads):
        """Worker thread para realizar a varredura"""
        try:
            scanner = PortScanner(timeout=timeout, max_threads=threads)
            
            # Atualiza progresso
            self.result_queue.put(("progress", f"Escaneando {len(targets)} host(s), {len(ports)} porta(s)"))
            
            # Realiza varredura
            results = scanner.scan_range(targets, ports, protocols)
            
            # Envia resultados
            for result in results:
                self.result_queue.put(("result", result))
            
            self.result_queue.put(("complete", f"Varredura concluída. {len(results)} portas verificadas."))
            
        except Exception as e:
            self.result_queue.put(("error", str(e)))
    
    def stop_scan(self):
        """Para a varredura"""
        self.scanning = False
        self.scan_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.progress_bar.stop()
        self.progress_var.set("Varredura interrompida")
    
    def check_queue(self):
        """Verifica messages da queue de resultados"""
        try:
            while True:
                msg_type, data = self.result_queue.get_nowait()
                
                if msg_type == "progress":
                    self.progress_var.set(data)
                elif msg_type == "result":
                    self.add_result(data)
                elif msg_type == "complete":
                    self.scan_complete(data)
                elif msg_type == "error":
                    self.scan_error(data)
        except queue.Empty:
            pass
        
        # Agenda próxima verificação
        self.root.after(100, self.check_queue)
    
    def add_result(self, result):
        """Adiciona resultado à tree view"""
        # Define cor baseada no status
        tags = []
        if result.status == "open":
            tags = ["open"]
        elif result.status == "closed":
            tags = ["closed"]
        elif "filtered" in result.status:
            tags = ["filtered"]
        
        # Adiciona à tree
        item = self.results_tree.insert("", tk.END, values=(
            result.host, result.port, result.protocol, result.status.upper()
        ), tags=tags)
        
        # Armazena resultado
        self.scan_results.append(result)
        
        # Configura cores
        self.results_tree.tag_configure("open", background="#d4edda")
        self.results_tree.tag_configure("closed", background="#f8d7da")
        self.results_tree.tag_configure("filtered", background="#fff3cd")
    
    def scan_complete(self, message):
        """Callback quando varredura completa"""
        self.scanning = False
        self.scan_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.progress_bar.stop()
        self.progress_var.set(message)
        
        # Mostra estatísticas
        open_count = len([r for r in self.scan_results if r.status == "open"])
        closed_count = len([r for r in self.scan_results if r.status == "closed"])
        filtered_count = len([r for r in self.scan_results if "filtered" in r.status])
        
        stats_message = f"Portas abertas: {open_count}, fechadas: {closed_count}, filtradas: {filtered_count}"
        messagebox.showinfo("Varredura Concluída", f"{message}\n\n{stats_message}")
    
    def scan_error(self, error_msg):
        """Callback quando há erro na varredura"""
        self.scanning = False
        self.scan_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.progress_bar.stop()
        self.progress_var.set("Erro na varredura")
        messagebox.showerror("Erro na Varredura", f"Erro durante a varredura:\n{error_msg}")
    
    def clear_results(self):
        """Limpa os resultados"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.scan_results = []
        self.progress_var.set("Resultados limpos")
    
    def save_results(self):
        """Salva os resultados em arquivo CSV"""
        if not self.scan_results:
            messagebox.showwarning("Aviso", "Nenhum resultado para salvar")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Salvar Resultados"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Host,Port,Protocol,Status\n")
                    for result in self.scan_results:
                        f.write(f"{result.host},{result.port},{result.protocol},{result.status}\n")
                
                messagebox.showinfo("Sucesso", f"Resultados salvos em:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{e}")


def main():
    """Função principal da GUI"""
    root = tk.Tk()
    app = PortScannerGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
