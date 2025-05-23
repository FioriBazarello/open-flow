import os
import threading
from src.ui.status_indicator import StatusIndicator
from src.utils.record import Record
from src.utils.speech_to_text import SpeechToText
from src.utils.clipboard import Clipboard
from src.utils.ollama_client import OllamaClient
from src.utils.prompt_manager import PromptManager

class Editor:
    def __init__(self, status_indicator: StatusIndicator):
        self.status_indicator = status_indicator
        self.editing = False
        self.selected_text = None
        self.ollama_client = OllamaClient()
        self.recorder = Record()
        self.speech_to_text = SpeechToText()
        self.prompt_manager = PromptManager()

    def start_edit_mode(self):
        if self.editing: return

        self.selected_text = Clipboard.read_from_clipboard()
        self.editing = True
        self.status_indicator.update_state('recording')
        self.recorder.start()

    def stop_edit_mode(self):
        if not self.editing: return

        self.status_indicator.update_state('processing')
        audio_file_path = self.recorder.stop()
        if not audio_file_path or not os.path.exists(audio_file_path):
            self.status_indicator.update_state('inactive')
            self.editing = False
            return
        try:
            transcribed_text = self.speech_to_text.transcribe(audio_file_path, language="pt")
            self._handle_transcription(transcribed_text)
        except Exception:
            self.status_indicator.update_state('error')
            self.editing = False
        finally:
            if audio_file_path and os.path.exists(audio_file_path):
                try:
                    os.unlink(audio_file_path)
                except PermissionError:
                    pass
            threading.Timer(1.5, lambda: self.status_indicator.update_state('inactive')).start()

    def toggle_edit_mode(self):
        if self.editing:
            self.stop_edit_mode()
        else:
            self.start_edit_mode()

    def _process_with_llm(self, original_text: str, instruction: str) -> str:
        prompt = self.prompt_manager.get_filled_prompt(
            'command_editor',
            original_text=original_text,
            instruction=instruction
        )
        try:
            edited_text = self.ollama_client.generate(prompt)
            if edited_text is not None:
                return edited_text
            else:
                self.status_indicator.update_state('error')
                return original_text
        except Exception:
            self.status_indicator.update_state('error')
            return original_text

    def _handle_transcription(self, transcribed_text: str):
        if not self.editing: return
        if not self.selected_text: return

        edited_text = self._process_with_llm(self.selected_text, transcribed_text)
        Clipboard.add_to_clipboard(edited_text)
        Clipboard.paste_hotkey()
        self.status_indicator.update_state('complete')
        self.selected_text = None
        self.editing = False
        threading.Timer(1.5, lambda: self.status_indicator.update_state('inactive')).start() 