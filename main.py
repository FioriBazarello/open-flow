import keyboard
from src.core.transcriber import Transcriber
from src.core.editor import Editor
from src.ui.system_tray import SystemTray
from src.config.settings import Settings
from src.ui.status_indicator import StatusIndicator
import threading

def main():
    feedback = StatusIndicator()
    transcriber = Transcriber(feedback, Settings.MODEL_NAME)
    command_editor = Editor(feedback)

    def keyboard_listener():
        keyboard.add_hotkey(Settings.HOTKEY, transcriber.toggle_recording)
        keyboard.add_hotkey(Settings.EDIT_HOTKEY, command_editor.toggle_edit_mode)
        print(f'✅ Pressione {Settings.HOTKEY} para iniciar a gravação.')
        print(f'✅ Pressione {Settings.HOTKEY} novamente para parar a gravação e transcrever.')
        print(f'✅ Pressione {Settings.EDIT_HOTKEY} para editar texto selecionado.')
        print("📌 O programa está rodando em background. Clique com o botão direito no ícone para sair.")
        keyboard.wait()  # Mantém o listener ativo

    def tray_runner():
        system_tray = SystemTray(icon_path="resources/icons/tray_icon.png")
        system_tray.run()

    threading.Thread(target=keyboard_listener, daemon=True).start()
    threading.Thread(target=tray_runner, daemon=True).start()
    feedback.root.mainloop()

if __name__ == "__main__":
    main()
