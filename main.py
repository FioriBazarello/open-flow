import keyboard
from src.core.transcriber import Transcriber
from src.core.command_editor import CommandEditor
from src.core.system_tray import SystemTray
from src.config.settings import Settings
from src.utils.feedback import FeedbackManager
import threading

def main():
    feedback = FeedbackManager()
    
    # Transcriber para transcrição normal (sem callback)
    transcriber = Transcriber(Settings.MODEL_NAME, feedback)
    
    # Transcriber específico para o CommandEditor (com callback)
    editor_transcriber = Transcriber(Settings.MODEL_NAME, feedback)
    command_editor = CommandEditor(editor_transcriber, feedback)

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
