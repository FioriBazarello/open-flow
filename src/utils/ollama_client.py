import requests

class OllamaClient:
    def __init__(self, url: str = "http://localhost:11434/api/generate", model: str = "phi4:latest"):
        self.url = url
        self.model = model

    def generate(self, prompt: str, stream: bool = False, timeout: int = 15) -> str:
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