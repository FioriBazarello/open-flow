import keyboard
import speech_recognition as sr
import pyperclip
import pyautogui
import threading
import pystray
from PIL import Image
import os

def transcrever_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Ouvindo...")
        audio = recognizer.listen(source)
    try:
        texto = recognizer.recognize_google(audio, language='pt-BR')
        print("📝 Transcrição:", texto)
        return texto
    except sr.UnknownValueError:
        print("😕 Não entendi o que foi dito.")
        return ""
    except sr.RequestError:
        print("🚫 Erro na conexão com o serviço.")
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
