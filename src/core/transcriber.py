import os
import threading
from typing import Callable
from src.utils.feedback import FeedbackManager
from src.utils.record import Record
from src.utils.speech_to_text import SpeechToText
from src.utils.clipboard import Clipboard

class Transcriber:
    def __init__(self, feedback: FeedbackManager, model_name="medium", on_transcription_complete: Callable | None = None):
        self.speech_to_text = SpeechToText(model_name)
        self.recorder = Record()
        self.feedback: FeedbackManager = feedback
        self.recording = False
        self.on_transcription_complete = on_transcription_complete

    def start_recording(self):
        if self.recording: return

        self.recording = True
        self.feedback.update_state('recording')
        self.feedback.play_sound('start')
        self.recorder.start()

    def stop_recording(self):
        if not self.recording: return

        self.recording = False
        self.feedback.update_state('processing')
        self.feedback.play_sound('stop')
        audio_file_path = self.recorder.stop()

        if not audio_file_path or not os.path.exists(audio_file_path):
            self.feedback.update_state('inactive')
            return

        try:
            transcribed_text = self.speech_to_text.transcribe(audio_file_path, language="pt")

            if self.on_transcription_complete:
                self.on_transcription_complete(transcribed_text)
            else:
                Clipboard.add_to_clipboard(transcribed_text)
                Clipboard.paste_hotkey()

            self.feedback.update_state('complete')
            self.feedback.play_sound('complete')

        except Exception:
            self.feedback.update_state('error')
            self.feedback.play_sound('error')

        finally:
            if audio_file_path and os.path.exists(audio_file_path):
                try:
                    os.unlink(audio_file_path)
                except PermissionError:
                    pass

            threading.Timer(1.5, lambda: self.feedback.update_state('inactive')).start()

    def toggle_recording(self):
        self.stop_recording() if self.recording else self.start_recording()