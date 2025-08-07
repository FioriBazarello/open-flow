from .config_manager import ConfigManager

class Settings:
    """Classe de configurações que usa o ConfigManager para persistência"""
    
    _config_manager = ConfigManager()
    
    @classmethod
    def get_model_name(cls) -> str:
        """Obtém o nome do modelo de transcrição"""
        return cls._config_manager.get_model_name()
    
    @classmethod
    def get_language(cls) -> str:
        """Obtém o idioma de transcrição"""
        return cls._config_manager.get_language()
    
    @classmethod
    def get_hotkey(cls) -> str:
        """Obtém o atalho de teclado para gravação"""
        return cls._config_manager.get_hotkey()
    
    @classmethod
    def get_edit_hotkey(cls) -> str:
        """Obtém o atalho de teclado para edição"""
        return cls._config_manager.get_edit_hotkey()
    
    @classmethod
    def set_model_name(cls, model_name: str) -> bool:
        """Define o nome do modelo de transcrição"""
        return cls._config_manager.set_model_name(model_name)
    
    @classmethod
    def set_language(cls, language: str) -> bool:
        """Define o idioma de transcrição"""
        return cls._config_manager.set_language(language)
    
    @classmethod
    def set_hotkey(cls, hotkey: str) -> bool:
        """Define o atalho de teclado para gravação"""
        return cls._config_manager.set_hotkey(hotkey)
    
    @classmethod
    def set_edit_hotkey(cls, edit_hotkey: str) -> bool:
        """Define o atalho de teclado para edição"""
        return cls._config_manager.set_edit_hotkey(edit_hotkey)
    
    @classmethod
    def get_all_config(cls) -> dict:
        """Obtém todas as configurações"""
        return cls._config_manager.get_all_config()
    
    @classmethod
    def reset_to_defaults(cls) -> bool:
        """Reseta todas as configurações para os valores padrão"""
        return cls._config_manager.reset_to_defaults()
    
    # Propriedades para compatibilidade com código existente
    @property
    def MODEL_NAME(self) -> str:
        return self.get_model_name()
    
    @property
    def LANGUAGE(self) -> str:
        return self.get_language()
    
    @property
    def HOTKEY(self) -> str:
        return self.get_hotkey()
    
    @property
    def EDIT_HOTKEY(self) -> str:
        return self.get_edit_hotkey() 