import os
import threading
from typing import Callable
from src.ui.status_indicator import StatusIndicator
from src.utils.record import Record
from src.utils.speech_to_text import SpeechToText
from src.utils.clipboard import Clipboard

class Transcriber:
    def __init__(self, status_indicator: StatusIndicator, model_name="medium", on_transcription_complete: Callable | None = None):
        self.speech_to_text = SpeechToText(model_name)
        self.recorder = Record()
        self.status_indicator: StatusIndicator = status_indicator
        self.recording = False
        self.on_transcription_complete = on_transcription_complete

    def start_recording(self):
        if self.recording: return

        self.recording = True
        self.status_indicator.update_state('recording')
        self.recorder.start()

    def stop_recording(self):
        if not self.recording: return

        self.recording = False
        self.status_indicator.update_state('processing')
        audio_file_path = self.recorder.stop()

        if not audio_file_path or not os.path.exists(audio_file_path):
            self.status_indicator.update_state('inactive')
            return

        try:
            transcribed_text = self.speech_to_text.transcribe(audio_file_path, language="pt")

            if self.on_transcription_complete:
                self.on_transcription_complete(transcribed_text)
            else:
                Clipboard.add_to_clipboard(transcribed_text)
                Clipboard.paste_hotkey()

            self.status_indicator.update_state('complete')

        except Exception:
            self.status_indicator.update_state('error')

        finally:
            if audio_file_path and os.path.exists(audio_file_path):
                try:
                    os.unlink(audio_file_path)
                except PermissionError:
                    pass

            threading.Timer(1.5, lambda: self.status_indicator.update_state('inactive')).start()

    def toggle_recording(self):
        self.stop_recording() if self.recording else self.start_recording()