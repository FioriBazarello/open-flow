import tkinter as tk
from tkinter import ttk
import os

class ConfigWindow:
    def __init__(self):
        self.root = None
        
    def create_window(self):
        """Cria e exibe a janela de configurações"""
        if self.root is not None:
            # Se a janela já existe, apenas traz para frente
            self.root.lift()
            self.root.focus_force()
            return
            
        self.root = tk.Tk()
        self.root.title("Open Flow - Configurações")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Centralizar a janela na tela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"600x400+{x}+{y}")
        
        # Configurar o protocolo de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Criar o conteúdo da janela
        self._create_content()
        
        # Iniciar a janela
        self.root.mainloop()
    
    def _create_content(self):
        """Cria o conteúdo da janela de configurações"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar grid weights
        if self.root:
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Configurações do Open Flow", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        # Seção de configurações gerais
        general_frame = ttk.LabelFrame(main_frame, text="Configurações Gerais", padding="10")
        general_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        general_frame.columnconfigure(1, weight=1)
        
        # Exemplo de configuração
        ttk.Label(general_frame, text="Servidor Ollama:").grid(row=0, column=0, sticky="w", pady=2)
        ollama_entry = ttk.Entry(general_frame, width=40)
        ollama_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=2)
        ollama_entry.insert(0, "http://localhost:11434")
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        save_button = ttk.Button(button_frame, text="Salvar", command=self._save_config)
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self._on_closing)
        cancel_button.pack(side=tk.LEFT)
        
        # Status bar
        status_label = ttk.Label(main_frame, text="Pronto", relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
    
    def _save_config(self):
        """Salva as configurações"""
        # TODO: Implementar salvamento das configurações
        print("Configurações salvas!")
    
    def _on_closing(self):
        """Manipula o fechamento da janela"""
        if self.root:
            self.root.destroy()
            self.root = None
