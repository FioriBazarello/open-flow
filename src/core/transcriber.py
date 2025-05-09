import whisper
import pyaudio
import tempfile
import os
import pyperclip
import pyautogui
import threading
import wave
import numpy as np

class Transcriber:
    def __init__(self, model_name="medium"):
        self.model = whisper.load_model(model_name)
        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.frames = []
            self.stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            print("🎙️ Gravando...")
            threading.Thread(target=self._record_audio).start()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            print("⏹️ Parando gravação...")
            self._process_audio()

    def _record_audio(self):
        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

    def _process_audio(self):
        if not self.frames:
            return

        temp_audio_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio_path = temp_audio.name
                wf = wave.open(temp_audio_path, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(self.frames))
                wf.close()

            # Agora que o arquivo está fechado, podemos fazer a transcrição
            resultado = self.model.transcribe(temp_audio_path, language="pt")
            texto = resultado["text"]
            print("📝 Transcrição:", texto)
            
            if texto:
                pyperclip.copy(texto)
                pyautogui.hotkey('ctrl', 'v')
        finally:
            # Garantimos que o arquivo seja deletado mesmo se houver erro
            if temp_audio_path and os.path.exists(temp_audio_path):
                try:
                    os.unlink(temp_audio_path)
                except PermissionError:
                    # Se ainda não conseguirmos deletar, ignoramos o erro
                    pass

    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording() 