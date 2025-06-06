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
        print(f"🎤 Transcriber inicializado com modelo: {model_name}")

    def start_recording(self):
        if self.recording: 
            print("⚠️  Gravação já está em andamento")
            return

        self.recording = True
        self.status_indicator.update_state('recording')
        self.recorder.start()
        print("🔴 INICIANDO GRAVAÇÃO...")
        print("🎙️  Fale agora - sua voz está sendo capturada")

    def stop_recording(self):
        if not self.recording: 
            print("⚠️  Nenhuma gravação ativa para parar")
            return

        self.recording = False
        print("⏹️  PARANDO GRAVAÇÃO...")
        self.status_indicator.update_state('processing')
        audio_file_path = self.recorder.stop()
        print(f"📁 Arquivo de áudio salvo: {audio_file_path}")

        if not audio_file_path or not os.path.exists(audio_file_path):
            print("❌ Erro: Arquivo de áudio não foi criado ou não existe")
            self.status_indicator.update_state('inactive')
            return

        try:
            print("🔄 PROCESSANDO TRANSCRIÇÃO...")
            print("🧠 Enviando áudio para o modelo de IA...")
            transcribed_text = self.speech_to_text.transcribe(audio_file_path, language="pt")
            
            print("=" * 60)
            print("📝 TEXTO TRANSCRITO:")
            print(f"'{transcribed_text}'")
            print("=" * 60)

            if self.on_transcription_complete:
                print("🔗 Enviando texto transcrito para callback personalizado")
                self.on_transcription_complete(transcribed_text)
            else:
                print("📋 Copiando texto para a área de transferência...")
                Clipboard.add_to_clipboard(transcribed_text)
                print("⌨️  Colando texto na aplicação ativa...")
                Clipboard.paste_hotkey()

            self.status_indicator.update_state('complete')
            print("✅ TRANSCRIÇÃO CONCLUÍDA COM SUCESSO!")

        except Exception as e:
            print(f"❌ ERRO DURANTE A TRANSCRIÇÃO: {str(e)}")
            self.status_indicator.update_state('error')

        finally:
            if audio_file_path and os.path.exists(audio_file_path):
                try:
                    os.unlink(audio_file_path)
                    print(f"🗑️  Arquivo temporário removido: {audio_file_path}")
                except PermissionError:
                    print(f"⚠️  Não foi possível remover arquivo temporário: {audio_file_path}")

            threading.Timer(1.5, lambda: self.status_indicator.update_state('inactive')).start()

    def toggle_recording(self):
        print("\n" + "="*50)
        if self.recording:
            print("🔄 ALTERNANDO: Parando gravação...")
            self.stop_recording()
        else:
            print("🔄 ALTERNANDO: Iniciando gravação...")
            self.start_recording()
        print("="*50 + "\n")