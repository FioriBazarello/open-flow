import keyboard
from src.core.transcriber import Transcriber
from src.core.editor import Editor
from src.ui.system_tray import SystemTray
from src.config.settings import Settings
from src.ui.status_indicator import StatusIndicator
import threading

def main():
    print("🚀 INICIANDO OPEN FLOW...")
    print("=" * 50)
    
    print("🎯 Carregando indicador de status...")
    feedback = StatusIndicator()
    
    print("🎤 Carregando transcriber...")
    transcriber = Transcriber(feedback, Settings.MODEL_NAME)
    
    print("✏️  Carregando editor...")
    command_editor = Editor(feedback)

    def keyboard_listener():
        print("⌨️  Configurando atalhos de teclado...")
        keyboard.add_hotkey(Settings.HOTKEY, transcriber.toggle_recording)
        keyboard.add_hotkey(Settings.EDIT_HOTKEY, command_editor.toggle_edit_mode)
        
        print("=" * 50)
        print("✅ SISTEMA PRONTO!")
        print(f'🎤 Pressione {Settings.HOTKEY} para iniciar a gravação.')
        print(f'🎤 Pressione {Settings.HOTKEY} novamente para parar a gravação e transcrever.')
        print(f'✏️  Pressione {Settings.EDIT_HOTKEY} para editar texto selecionado.')
        print("📌 O programa está rodando em background. Clique com o botão direito no ícone para sair.")
        print("=" * 50)
        
        keyboard.wait()  # Mantém o listener ativo

    def tray_runner():
        print("🔧 Carregando system tray...")
        system_tray = SystemTray(icon_path="resources/icons/tray_icon.png")
        system_tray.run()

    print("🔄 Iniciando threads do sistema...")
    threading.Thread(target=keyboard_listener, daemon=True).start()
    threading.Thread(target=tray_runner, daemon=True).start()
    
    print("🎯 Interface iniciada - sistema operacional!")
    feedback.root.mainloop()

if __name__ == "__main__":
    main()
