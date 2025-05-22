import requests
import threading
from src.utils.feedback import FeedbackManager
from src.utils.record import Record
from src.utils.speech_to_text import SpeechToText
from src.utils.clipboard import Clipboard
import os

class CommandEditor:
    def __init__(self, feedback: FeedbackManager):
        self.feedback = feedback
        self.editing = False
        self.selected_text = None
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "phi4:latest"
        self.recorder = Record()
        self.speech_to_text = SpeechToText()

    def start_edit_mode(self):
        if self.editing: return

        self.selected_text = Clipboard.read_from_clipboard()
        self.editing = True
        self.feedback.update_state('recording')
        self.recorder.start()

    def stop_edit_mode(self):
        if not self.editing: return

        self.feedback.update_state('processing')
        audio_file_path = self.recorder.stop()
        if not audio_file_path or not os.path.exists(audio_file_path):
            self.feedback.update_state('inactive')
            self.editing = False
            return
        try:
            transcribed_text = self.speech_to_text.transcribe(audio_file_path, language="pt")
            self._handle_transcription(transcribed_text)
        except Exception:
            self.feedback.update_state('error')
            self.feedback.play_sound('error')
            self.editing = False
        finally:
            if audio_file_path and os.path.exists(audio_file_path):
                try:
                    os.unlink(audio_file_path)
                except PermissionError:
                    pass
            threading.Timer(1.5, lambda: self.feedback.update_state('inactive')).start()

    def toggle_edit_mode(self):
        if self.editing:
            self.stop_edit_mode()
        else:
            self.start_edit_mode()

    def _process_with_llm(self, original_text: str, instruction: str) -> str:
        prompt = f"""Você é um assistente de edição de texto. Sua tarefa é editar o texto fornecido de acordo com a instrução.

REGRAS IMPORTANTES:
1. Mantenha TODO o conteúdo e significado original do texto, a menos que a instrução especifique explicitamente para adicionar ou remover informações.
2. Você deve focar apenas em ajustes de:
   - Pontuação
   - Formato
   - Linguagem
   - Estrutura
   - Idioma
3. Responda APENAS com o texto editado, sem aspas, sem formatação adicional, sem explicações.
4. NÃO inclua palavras como "Texto editado:" ou qualquer outro texto além do resultado da edição.

Texto original:
{original_text}

Instrução de edição:
{instruction}

Responda apenas com o texto editado:"""
        try:
            response = requests.post(
                 self.ollama_url,
                 json={
                     "model": self.model,
                     "prompt": prompt,
                     "stream": False
                },
                timeout=15
             )
            if response.status_code == 200:
                result = response.json()
                edited_text = result.get('response', '').strip()
                edited_text = edited_text.strip('"\'')
                return edited_text
            else:
                self.feedback.update_state('error')
                self.feedback.play_sound('error')
                return original_text
        except Exception:
            self.feedback.update_state('error')
            self.feedback.play_sound('error')
            return original_text

    def _handle_transcription(self, transcribed_text: str):
        if not self.editing: return
        if not self.selected_text: return

        edited_text = self._process_with_llm(self.selected_text, transcribed_text)
        Clipboard.add_to_clipboard(edited_text)
        Clipboard.paste_hotkey()
        self.feedback.update_state('complete')
        self.feedback.play_sound('complete')
        self.selected_text = None
        self.editing = False
        threading.Timer(1.5, lambda: self.feedback.update_state('inactive')).start() 