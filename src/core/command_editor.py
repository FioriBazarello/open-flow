import pyperclip
import pyautogui
import keyboard
import requests
import json
import threading
from src.core.transcriber import Transcriber
from src.utils.feedback import FeedbackManager
import time

class CommandEditor:
    def __init__(self, transcriber: Transcriber, feedback: FeedbackManager):
        self.transcriber = transcriber
        self.feedback = feedback
        self.editing = False
        self.selected_text = None
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "phi4:latest"
        
        # Configura o callback do Transcriber
        self.transcriber.on_transcription_complete = self._handle_transcription
        print("🔧 CommandEditor inicializado")

    def start_edit_mode(self):
        """Inicia o modo de edição, capturando o texto selecionado"""
        if self.editing:
            print("⚠️ Modo de edição já está ativo")
            return

        print("📝 Iniciando modo de edição...")
        
        # Limpa a área de transferência antes de copiar
        # pyperclip.copy('')
        
        # Simula o Ctrl+C de forma mais confiável
        keyboard.press('ctrl')
        keyboard.press('c')
        keyboard.release('c')
        keyboard.release('ctrl')
        
        # Pequeno delay para garantir que o texto foi copiado
        time.sleep(0.2)  # Aumentei o delay para dar mais tempo
        
        self.selected_text = pyperclip.paste()
        
        print(f"📋 Texto selecionado: {self.selected_text}")
        
        if not self.selected_text:
            print("❌ Nenhum texto selecionado!")
            self.feedback.update_state('error')
            self.feedback.play_sound('error')
            return

        self.editing = True
        print(f"✅ Modo de edição ativado: {self.editing}")
        self.feedback.update_state('editing')
        self.feedback.play_sound('start')
        
        # Inicia a gravação do comando
        print("🎙️ Iniciando gravação do comando...")
        self.transcriber.start_recording()

    def _process_with_llm(self, original_text: str, instruction: str) -> str:
        """Processa o texto usando o Ollama LLM"""
        print(f"🤖 Processando com LLM...")
        print(f"📝 Texto original: {original_text}")
        print(f"📝 Instrução: {instruction}")
        
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
            print(f"🌐 Enviando requisição para Ollama...")
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                edited_text = result.get('response', '').strip()
                # Remove possíveis aspas ou formatação adicional
                edited_text = edited_text.strip('"\'')
                print(f"✅ Texto editado recebido: {edited_text}")
                return edited_text
            else:
                print(f"❌ Erro na requisição: {response.status_code}")
                print(f"Resposta: {response.text}")
                self.feedback.update_state('error')
                self.feedback.play_sound('error')
                return original_text
                
        except Exception as e:
            print(f"❌ Erro ao processar com LLM: {str(e)}")
            self.feedback.update_state('error')
            self.feedback.play_sound('error')
            return original_text

    def _handle_transcription(self, transcribed_text: str):
        """Callback chamado quando a transcrição está pronta"""
        print(f"🎯 Callback de transcrição recebido: {transcribed_text}")
        print(f"📊 Estado de edição: {self.editing}")
        print(f"📊 Texto selecionado existe: {self.selected_text is not None}")
        
        if not self.editing:
            print("⚠️ Callback recebido mas modo de edição não está ativo!")
            return
            
        if not self.selected_text:
            print("⚠️ Callback recebido mas não há texto selecionado!")
            return

        print("🔄 Iniciando processamento do texto...")
        edited_text = self._process_with_llm(
            self.selected_text, 
            transcribed_text
        )
        
        print("📋 Colando texto editado...")
        # Cola o texto editado
        pyperclip.copy(edited_text)
        pyautogui.hotkey('ctrl', 'v')
        
        self.feedback.update_state('complete')
        self.feedback.play_sound('complete')
        
        # Limpa as variáveis
        self.selected_text = None
        self.editing = False
        print("✨ Processo de edição concluído")
        
        # Volta para inativo depois de um tempo
        threading.Timer(1.5, lambda: self.feedback.update_state('inactive')).start()

    def stop_edit_mode(self):
        """Para o modo de edição e processa o comando"""
        if not self.editing:
            print("⚠️ Tentativa de parar modo de edição quando não está ativo")
            return

        print("⏹️ Parando modo de edição...")
        # Não alteramos self.editing aqui, pois precisamos dele no callback
        self.transcriber.stop_recording()
        self.feedback.update_state('processing')

    def toggle_edit_mode(self):
        """Alterna entre iniciar e parar o modo de edição"""
        print(f"🔄 Alternando modo de edição. Estado atual: {self.editing}")
        if self.editing:
            self.stop_edit_mode()
        else:
            self.start_edit_mode() 