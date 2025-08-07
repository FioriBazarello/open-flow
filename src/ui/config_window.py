import tkinter as tk
from tkinter import ttk
import os
from src.config.settings import Settings

class ConfigWindow:
    def __init__(self):
        self.root = None
        self.model_var = None
        self.language_var = None
        self.ollama_entry = None
        self.status_label = None
        self.model_desc_label = None
        self.language_desc_label = None
        
        # Propriedades para os comboboxes
        self.model_combo = None
        self.language_combo = None
        
        # Dicionários para mapear valores para descrições
        self.model_descriptions = {
            "tiny": "Muito rápido, menos preciso",
            "base": "Equilibrado",
            "small": "Boa precisão",
            "medium": "Muito boa precisão (recomendado)",
            "large": "Melhor precisão, mais lento"
        }
        
        self.language_descriptions = {
            "pt": "Português",
            "en": "Inglês", 
            "es": "Espanhol",
            "fr": "Francês",
            "de": "Alemão",
            "it": "Italiano",
            "auto": "Detecção automática"
        }
        
    def create_window(self):
        """Cria e exibe a janela de configurações"""
        if self.root is not None:
            # Se a janela já existe, apenas traz para frente
            self.root.lift()
            self.root.focus_force()
            return
            
        self.root = tk.Tk()
        self.root.title("Open Flow - Configurações")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Centralizar a janela na tela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (550 // 2)
        self.root.geometry(f"700x550+{x}+{y}")
        
        # Configurar o protocolo de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Criar o conteúdo da janela
        self._create_content()
        
        # Carregar configurações atuais
        self._load_current_config()
        
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
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")
        
        # Seção de configurações de transcrição
        transcription_frame = ttk.LabelFrame(main_frame, text="Configurações de Transcrição", padding="15")
        transcription_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        transcription_frame.columnconfigure(1, weight=1)
        
        # Modelo de transcrição
        ttk.Label(transcription_frame, text="Modelo:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.model_var = tk.StringVar(value="medium")
        self.model_combo = ttk.Combobox(transcription_frame, textvariable=self.model_var, 
                                   values=["tiny", "base", "small", "medium", "large"], 
                                   state="readonly", width=20, font=("Arial", 10))
        self.model_combo.grid(row=0, column=1, sticky="w", padx=(15, 0), pady=5)
        # Definir valor padrão
        self.model_combo.set("medium")
        
        # Descrição do modelo atual
        self.model_desc_label = ttk.Label(transcription_frame, text="", 
                                         font=("Arial", 9), foreground="blue")
        self.model_desc_label.grid(row=0, column=2, sticky="w", padx=(10, 0), pady=5)
        
        # Idioma de transcrição
        ttk.Label(transcription_frame, text="Idioma:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.language_var = tk.StringVar(value="pt")
        self.language_combo = ttk.Combobox(transcription_frame, textvariable=self.language_var,
                                      values=["pt", "en", "es", "fr", "de", "it", "auto"],
                                      state="readonly", width=20, font=("Arial", 10))
        self.language_combo.grid(row=1, column=1, sticky="w", padx=(15, 0), pady=5)
        # Definir valor padrão
        self.language_combo.set("pt")
        
        # Descrição do idioma atual
        self.language_desc_label = ttk.Label(transcription_frame, text="", 
                                           font=("Arial", 9), foreground="blue")
        self.language_desc_label.grid(row=1, column=2, sticky="w", padx=(10, 0), pady=5)
        
        # Configurar callbacks para atualizar descrições
        self.model_combo.bind('<<ComboboxSelected>>', self._on_model_changed)
        self.language_combo.bind('<<ComboboxSelected>>', self._on_language_changed)
        
        # Seção de configurações gerais
        general_frame = ttk.LabelFrame(main_frame, text="Configurações Gerais", padding="15")
        general_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        general_frame.columnconfigure(1, weight=1)
        
        # Servidor Ollama
        ttk.Label(general_frame, text="Servidor Ollama:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.ollama_entry = ttk.Entry(general_frame, width=50, font=("Arial", 10))
        self.ollama_entry.grid(row=0, column=1, sticky="ew", padx=(15, 0), pady=5)
        self.ollama_entry.insert(0, "http://localhost:11434")
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(20, 0))
        
        save_button = ttk.Button(button_frame, text="Salvar Configurações", command=self._save_config, style="Accent.TButton")
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self._on_closing)
        cancel_button.pack(side=tk.LEFT)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Pronto", relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 9))
        self.status_label.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(15, 0))
    
    def _on_model_changed(self, event=None):
        """Callback quando o modelo é alterado"""
        print(f"🔍 DEBUG: Callback _on_model_changed chamado!")
        if self.model_combo:
            novo_modelo = self.model_combo.get()
            print(f"🔍 DEBUG: Novo modelo selecionado: {novo_modelo}")
            # Atualizar a StringVar manualmente
            if self.model_var:
                self.model_var.set(novo_modelo)
            # Atualizar a descrição
            self._update_model_description()
    
    def _update_model_description(self):
        """Atualiza a descrição do modelo"""
        if self.model_combo and self.model_desc_label:
            current_model = self.model_combo.get()
            print(f"🔍 DEBUG: Modelo atual: {current_model}")
            if current_model in self.model_descriptions:
                self.model_desc_label.config(text=self.model_descriptions[current_model])
                print(f"🔍 DEBUG: Descrição atualizada para: {self.model_descriptions[current_model]}")
    
    def _on_language_changed(self, event=None):
        """Callback quando o idioma é alterado"""
        print(f"🔍 DEBUG: Callback _on_language_changed chamado!")
        if self.language_combo:
            novo_idioma = self.language_combo.get()
            print(f"🔍 DEBUG: Novo idioma selecionado: {novo_idioma}")
            # Atualizar a StringVar manualmente
            if self.language_var:
                self.language_var.set(novo_idioma)
            # Atualizar a descrição
            self._update_language_description()
    
    def _update_language_description(self):
        """Atualiza a descrição do idioma"""
        if self.language_combo and self.language_desc_label:
            current_language = self.language_combo.get()
            print(f"🔍 DEBUG: Idioma atual: {current_language}")
            if current_language in self.language_descriptions:
                self.language_desc_label.config(text=self.language_descriptions[current_language])
                print(f"🔍 DEBUG: Descrição atualizada para: {self.language_descriptions[current_language]}")
    
    def _load_current_config(self):
        """Carrega as configurações atuais nos campos"""
        try:
            print("🔍 DEBUG: Iniciando carregamento de configurações...")
            
            # Carregar modelo atual
            current_model = Settings.get_model_name()
            print(f"🔍 DEBUG: Modelo carregado das configurações: {current_model}")
            
            if self.model_combo:
                print(f"🔍 DEBUG: Definindo modelo na interface: {current_model}")
                self.model_combo.set(current_model)
                # Atualizar StringVar também
                if self.model_var:
                    self.model_var.set(current_model)
                # Atualizar descrição imediatamente
                self._update_model_description()
            else:
                print("❌ DEBUG: model_combo é None!")
            
            # Carregar idioma atual
            current_language = Settings.get_language()
            print(f"🔍 DEBUG: Idioma carregado das configurações: {current_language}")
            
            if self.language_combo:
                print(f"🔍 DEBUG: Definindo idioma na interface: {current_language}")
                self.language_combo.set(current_language)
                # Atualizar StringVar também
                if self.language_var:
                    self.language_var.set(current_language)
                # Atualizar descrição imediatamente
                self._update_language_description()
            else:
                print("❌ DEBUG: language_combo é None!")
            
            self._update_status("Configurações carregadas com sucesso")
            print("✅ DEBUG: Carregamento concluído com sucesso")
        except Exception as e:
            print(f"❌ DEBUG: Erro ao carregar configurações: {str(e)}")
            self._update_status(f"Erro ao carregar configurações: {str(e)}")
    
    def _save_config(self):
        """Salva as configurações"""
        try:
            print("🔍 DEBUG: Iniciando salvamento de configurações...")
            
            # Debug: mostrar valores atuais dos comboboxes
            if self.model_combo:
                print(f"🔍 DEBUG: Valor atual de model_combo: '{self.model_combo.get()}'")
            else:
                print("❌ DEBUG: model_combo é None!")
                
            if self.language_combo:
                print(f"🔍 DEBUG: Valor atual de language_combo: '{self.language_combo.get()}'")
            else:
                print("❌ DEBUG: language_combo é None!")
            
            # Salvar modelo
            if self.model_combo:
                new_model = self.model_combo.get()
                print(f"🔍 DEBUG: Modelo a ser salvo: {new_model}")
                if new_model:
                    success = Settings.set_model_name(new_model)
                    print(f"🔍 DEBUG: Salvamento do modelo: {'✅' if success else '❌'}")
                else:
                    print("❌ DEBUG: Modelo está vazio!")
            else:
                print("❌ DEBUG: model_combo é None!")
            
            # Salvar idioma
            if self.language_combo:
                new_language = self.language_combo.get()
                print(f"🔍 DEBUG: Idioma a ser salvo: {new_language}")
                if new_language:
                    success = Settings.set_language(new_language)
                    print(f"🔍 DEBUG: Salvamento do idioma: {'✅' if success else '❌'}")
                else:
                    print("❌ DEBUG: Idioma está vazio!")
            else:
                print("❌ DEBUG: language_combo é None!")
            
            self._update_status("Configurações salvas com sucesso!")
            print("✅ DEBUG: Salvamento concluído com sucesso")
            
            # Fechar a janela após salvar
            self._on_closing()
            
        except Exception as e:
            print(f"❌ DEBUG: Erro ao salvar configurações: {str(e)}")
            self._update_status(f"Erro ao salvar configurações: {str(e)}")
    
    def _update_status(self, message: str):
        """Atualiza a mensagem de status"""
        if self.status_label:
            self.status_label.config(text=message)
    
    def _on_closing(self):
        """Manipula o fechamento da janela"""
        if self.root:
            self.root.destroy()
            self.root = None
