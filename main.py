import keyboard
from src.core.transcriber import Transcriber
from src.core.system_tray import SystemTray
from src.config.settings import Settings

def main():
    transcriber = Transcriber(Settings.MODEL_NAME)
    keyboard.add_hotkey(Settings.HOTKEY, transcriber.toggle_recording)
    print(f'✅ Pressione {Settings.HOTKEY} para iniciar a gravação.')
    print(f'✅ Pressione {Settings.HOTKEY} novamente para parar a gravação e transcrever.')
    print("📌 O programa está rodando em background. Clique com o botão direito no ícone para sair.")
    system_tray = SystemTray()
    system_tray.run()

if __name__ == "__main__":
    main()
