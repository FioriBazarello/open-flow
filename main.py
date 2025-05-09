import keyboard
import speech_recognition as sr
import pyperclip
import pyautogui
import threading
import pystray
from PIL import Image
import os
import whisper
import tempfile

# Carregar o modelo Whisper (você pode escolher entre 'tiny', 'base', 'small', 'medium', 'large')
modelo_whisper = whisper.load_model("base")

def transcrever_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Ouvindo...")
        audio = recognizer.listen(source)
    
    try:
        # Salvar o áudio temporariamente
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio.get_wav_data())
            temp_audio_path = temp_audio.name

        # Transcrever usando Whisper
        resultado = modelo_whisper.transcribe(temp_audio_path, language="pt")
        texto = resultado["text"]
        
        # Limpar o arquivo temporário
        os.unlink(temp_audio_path)
        
        print("📝 Transcrição:", texto)
        return texto
    except Exception as e:
        print(f"🚫 Erro na transcrição: {str(e)}")
        return ""

def iniciar_transcricao():
    texto = transcrever_audio()
    if texto:
        pyperclip.copy(texto)
        pyautogui.hotkey('ctrl', 'v')

# Rodar em thread pra não travar o hotkey
def ativar_transcricao():
    threading.Thread(target=iniciar_transcricao).start()

def criar_icone():
    # Criar um ícone simples (um quadrado branco)
    image = Image.new('RGB', (64, 64), 'white')
    
    def on_exit(icon, item):
        icon.stop()
        os._exit(0)
    
    menu = pystray.Menu(
        pystray.MenuItem('Sair', on_exit)
    )
    
    icon = pystray.Icon("open-flow", image, "Open Flow", menu)
    return icon

def main():
    keyboard.add_hotkey('ctrl+alt', ativar_transcricao)
    print("✅ Segure Ctrl+Alt, fale, e solte...")
    print("📌 O programa está rodando em background. Clique com o botão direito no ícone para sair.")
    
    icon = criar_icone()
    icon.run()

if __name__ == "__main__":
    main()
