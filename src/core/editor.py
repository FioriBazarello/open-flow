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
        print("✏️  Editor inicializado e pronto para editar textos")

    def start_edit_mode(self):
        if self.editing: 
            print("⚠️  Modo de edição já está ativo")
            return

        print("\n" + "="*60)
        print("✏️  INICIANDO MODO DE EDIÇÃO...")
        self.selected_text = Clipboard.read_from_clipboard()
        if not self.selected_text:
            print("⚠️  Nenhum texto copiado/selecionado. Abortando modo de edição")
            self.status_indicator.update_state('inactive')
            return
        
        print("📋 TEXTO SELECIONADO CAPTURADO:")
        print(f"'{self.selected_text}'")
        print("-" * 60)
        
        self.editing = True
        self.status_indicator.update_state('recording')
        self.recorder.start()
        print("🔴 GRAVANDO INSTRUÇÃO DE EDIÇÃO...")
        print("🎙️  Fale sua instrução de como editar o texto")

    def stop_edit_mode(self):
        if not self.editing: 
            print("⚠️  Modo de edição não está ativo")
            return

        print("⏹️  PARANDO GRAVAÇÃO DA INSTRUÇÃO...")
        self.status_indicator.update_state('processing')
        audio_file_path = self.recorder.stop()
        print(f"📁 Arquivo de áudio da instrução salvo: {audio_file_path}")
        
        if not audio_file_path or not os.path.exists(audio_file_path):
            print("❌ Erro: Arquivo de áudio da instrução não foi criado")
            self.status_indicator.update_state('inactive')
            self.editing = False
            return
            
        try:
            print("🔄 TRANSCREVENDO INSTRUÇÃO DE EDIÇÃO...")
            transcribed_text = self.speech_to_text.transcribe(audio_file_path, language="pt")
            print("🎯 INSTRUÇÃO TRANSCRITA:")
            print(f"'{transcribed_text}'")
            print("-" * 60)
            
            self._handle_transcription(transcribed_text)
        except Exception as e:
            print(f"❌ ERRO DURANTE TRANSCRIÇÃO DA INSTRUÇÃO: {str(e)}")
            self.status_indicator.update_state('error')
            self.editing = False
        finally:
            if audio_file_path and os.path.exists(audio_file_path):
                try:
                    os.unlink(audio_file_path)
                    print(f"🗑️  Arquivo temporário da instrução removido: {audio_file_path}")
                except PermissionError:
                    print(f"⚠️  Não foi possível remover arquivo temporário: {audio_file_path}")
            threading.Timer(1.5, lambda: self.status_indicator.update_state('inactive')).start()

    def toggle_edit_mode(self):
        print("\n" + "="*50)
        if self.editing:
            print("🔄 ALTERNANDO: Finalizando edição...")
            self.stop_edit_mode()
        else:
            print("🔄 ALTERNANDO: Iniciando edição...")
            self.start_edit_mode()
        print("="*50 + "\n")

    def _process_with_llm(self, original_text: str, instruction: str) -> str:
        print("🤖 PROCESSANDO COM IA...")
        print("📤 Enviando para o modelo de linguagem:")
        print(f"   📄 Texto original: '{original_text[:50]}{'...' if len(original_text) > 50 else ''}'")
        print(f"   🎯 Instrução: '{instruction}'")
        
        prompt = self.prompt_manager.get_filled_prompt(
            'editor',
            original_text=original_text,
            instruction=instruction
        )
        
        try:
            print("⏳ Aguardando resposta do modelo...")
            edited_text = self.ollama_client.generate(prompt)
            if edited_text is not None:
                print("✅ Texto editado com sucesso pela IA!")
                return edited_text
            else:
                print("❌ IA retornou resposta vazia - mantendo texto original")
                self.status_indicator.update_state('error')
                self.editing = False
                return original_text
        except Exception as e:
            print(f"❌ ERRO NA COMUNICAÇÃO COM IA: {str(e)}")
            print("🔄 Mantendo texto original devido ao erro")
            self.status_indicator.update_state('error')
            self.editing = False
            return original_text

    def _handle_transcription(self, transcribed_text: str):
        if not self.editing: 
            print("⚠️  Edição não está ativa - ignorando transcrição")
            return
        if not self.selected_text: 
            print("⚠️  Nenhum texto selecionado - ignorando transcrição")
            self.status_indicator.update_state('inactive')
            self.editing = False
            return

        print("🔄 INICIANDO PROCESSO DE EDIÇÃO...")
        edited_text = self._process_with_llm(self.selected_text, transcribed_text)
        
        print("=" * 60)
        print("📝 RESULTADO FINAL DA EDIÇÃO:")
        print(f"'{edited_text}'")
        print("=" * 60)
        
        print("📋 Copiando texto editado para área de transferência...")
        Clipboard.add_to_clipboard(edited_text)
        print("⌨️  Colando texto editado na aplicação...")
        Clipboard.paste_hotkey()
        
        self.status_indicator.update_state('complete')
        print("✅ EDIÇÃO CONCLUÍDA COM SUCESSO!")
        
        self.selected_text = None
        self.editing = False
        threading.Timer(1.5, lambda: self.status_indicator.update_state('inactive')).start() 