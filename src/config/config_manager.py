import json
import os
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Gerenciador de configurações persistentes do usuário"""
    
    def __init__(self, config_file: str = "user_config.json"):
        # Determina o diretório de configuração
        self.config_dir = Path(__file__).parent
        self.config_file = self.config_dir / config_file
        self.default_config = {
            "model_name": "medium",
            "language": "pt",
            "ollama_base_url": "http://localhost:11434",
            "hotkey": "ctrl+alt",
            "edit_hotkey": "ctrl+windows"
        }
        self._config = None
    
    def load_config(self) -> Dict[str, Any]:
        """Carrega as configurações do arquivo JSON ou retorna as padrão"""
        if self._config is not None:
            return self._config
            
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Mescla com configurações padrão para garantir que todos os campos existam
                    self._config = {**self.default_config, **loaded_config}
                    print(f"📁 Configurações carregadas de: {self.config_file}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  Erro ao carregar configurações: {e}")
                print("🔄 Usando configurações padrão")
                self._config = self.default_config.copy()
        else:
            print("📁 Arquivo de configuração não encontrado")
            print("🔄 Usando configurações padrão")
            self._config = self.default_config.copy()
            # Cria o arquivo com as configurações padrão
            self.save_config()
        
        return self._config
    
    def save_config(self, config: Dict[str, Any] | None = None) -> bool:
        """Salva as configurações no arquivo JSON"""
        if config is not None:
            self._config = config
        
        if self._config is None:
            self._config = self.load_config()
        
        try:
            # Garante que o diretório existe
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Configurações salvas em: {self.config_file}")
            return True
        except IOError as e:
            print(f"❌ Erro ao salvar configurações: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtém um valor de configuração específico"""
        config = self.load_config()
        return config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Define um valor de configuração específico"""
        config = self.load_config()
        config[key] = value
        return self.save_config(config)
    
    def get_model_name(self) -> str:
        """Obtém o nome do modelo de transcrição"""
        return self.get("model_name", "medium")
    
    def get_language(self) -> str:
        """Obtém o idioma de transcrição"""
        return self.get("language", "pt")
    
    def get_hotkey(self) -> str:
        """Obtém o atalho de teclado para gravação"""
        return self.get("hotkey", "ctrl+alt")
    
    def get_edit_hotkey(self) -> str:
        """Obtém o atalho de teclado para edição"""
        return self.get("edit_hotkey", "ctrl+windows")
    
    def get_ollama_base_url(self) -> str:
        """Obtém a URL base do servidor Ollama"""
        return self.get("ollama_base_url", "http://localhost:11434")
    
    def set_model_name(self, model_name: str) -> bool:
        """Define o nome do modelo de transcrição"""
        return self.set("model_name", model_name)
    
    def set_language(self, language: str) -> bool:
        """Define o idioma de transcrição"""
        return self.set("language", language)
    
    def set_hotkey(self, hotkey: str) -> bool:
        """Define o atalho de teclado para gravação"""
        return self.set("hotkey", hotkey)
    
    def set_edit_hotkey(self, edit_hotkey: str) -> bool:
        """Define o atalho de teclado para edição"""
        return self.set("edit_hotkey", edit_hotkey)
    
    def set_ollama_base_url(self, url: str) -> bool:
        """Define a URL base do servidor Ollama"""
        return self.set("ollama_base_url", url)
    
    def get_all_config(self) -> Dict[str, Any]:
        """Obtém todas as configurações"""
        return self.load_config().copy()
    
    def reset_to_defaults(self) -> bool:
        """Reseta todas as configurações para os valores padrão"""
        self._config = self.default_config.copy()
        return self.save_config()
