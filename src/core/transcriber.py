import whisper
import pyaudio
import tempfile
import os
import pyperclip
import pyautogui
import threading
import wave
import numpy as np
import sys
from src.utils.feedback import FeedbackManager

class Transcriber:
    def __init__(self, model_name="medium", feedback=None, on_transcription_complete=None):
        print("🔧 Inicializando Transcriber...")
        self.model = whisper.load_model(model_name)
        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        if feedback is None:
            raise ValueError('FeedbackManager deve ser passado para Transcriber')
        self.feedback = feedback
        self.on_transcription_complete = on_transcription_complete
        print("✅ Transcriber inicializado com sucesso")

    def start_recording(self):
        if not self.recording:
            print("🎙️ Iniciando gravação...")
            self.recording = True
            self.frames = []
            self.stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            self.feedback.update_state('recording')
            self.feedback.play_sound('start')
            print("✅ Stream de áudio aberto")
            threading.Thread(target=self._record_audio).start()

    def stop_recording(self):
        if self.recording:
            print("⏹️ Parando gravação...")
            self.recording = False
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                print("✅ Stream de áudio fechado")
            self.feedback.update_state('processing')
            self.feedback.play_sound('stop')
            print("🔄 Iniciando processamento do áudio...")
            self._process_audio()

    def _record_audio(self):
        print("🎵 Iniciando captura de áudio...")
        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
        print(f"✅ Captura de áudio concluída. {len(self.frames)} frames coletados")

    def _process_audio(self):
        if not self.frames:
            print("⚠️ Nenhum frame de áudio para processar")
            self.feedback.update_state('inactive')
            return

        temp_audio_path = None
        try:
            print("💾 Salvando áudio em arquivo temporário...")
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio_path = temp_audio.name
                wf = wave.open(temp_audio_path, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(self.frames))
                wf.close()
            print(f"✅ Áudio salvo em: {temp_audio_path}")

            self.feedback.update_state('processing')
            print("🤖 Iniciando transcrição com Whisper...")
            resultado = self.model.transcribe(temp_audio_path, language="pt")
            texto = resultado["text"]
            print(f"📝 Texto transcrito: {texto}")
            
            if texto:
                if self.on_transcription_complete:
                    print("🔄 Chamando callback de transcrição...")
                    self.on_transcription_complete(texto)
                else:
                    print("📋 Copiando texto para área de transferência...")
                    pyperclip.copy(texto)
                    pyautogui.hotkey('ctrl', 'v')
                    
            self.feedback.update_state('complete')
            self.feedback.play_sound('complete')
            print("✅ Processamento concluído com sucesso")
        except Exception as e:
            print(f"❌ Erro durante o processamento: {str(e)}")
            self.feedback.update_state('error')
            self.feedback.play_sound('error')
        finally:
            if temp_audio_path and os.path.exists(temp_audio_path):
                try:
                    os.unlink(temp_audio_path)
                    print("🧹 Arquivo temporário removido")
                except PermissionError:
                    print("⚠️ Não foi possível remover o arquivo temporário")
            threading.Timer(1.5, lambda: self.feedback.update_state('inactive')).start()

    def toggle_recording(self):
        if self.recording:
            print("🔄 Alternando: parando gravação")
            self.stop_recording()
        else:
            print("🔄 Alternando: iniciando gravação")
            self.start_recording() 