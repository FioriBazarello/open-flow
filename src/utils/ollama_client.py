import requests
from src.config.settings import Settings

class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str = "phi4:latest"):
        # Usa a URL configurada pelo usuário caso não seja informada
        resolved_base_url = (base_url or Settings.get_ollama_base_url()).rstrip("/")
        # Garante que o endpoint correto seja utilizado
        if resolved_base_url.endswith("/api/generate"):
            self.url = resolved_base_url
        elif resolved_base_url.endswith("/api") or resolved_base_url.endswith("/api/"):
            self.url = f"{resolved_base_url.rstrip('/')}" + "/generate"
        else:
            self.url = f"{resolved_base_url}" + "/api/generate"
        self.model = model

    def generate(self, prompt: str, stream: bool = False, timeout: int = 15) -> str | None:
        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": stream
                },
                timeout=timeout
            )
            if response.status_code == 200:
                result = response.json()
                edited_text = result.get('response', '').strip()
                edited_text = edited_text.strip('"\'')
                return edited_text
            else:
                return None
        except Exception:
            return None 