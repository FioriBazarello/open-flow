import pystray
from PIL import Image
import os
import sys
import tkinter as tk
from .config_window import ConfigWindow

class SystemTray:
    def __init__(self, icon_path=None, tk_root: tk.Tk | None = None):
        self.icon_path = icon_path
        self.tk_root = tk_root
        self.config_window = ConfigWindow(master=self.tk_root)
        self.icon = self._create_icon()

    def _create_icon(self):
        if self.icon_path and os.path.exists(self.icon_path):
            image = Image.open(self.icon_path)
            image = image.resize((64, 64), Image.Resampling.LANCZOS)
        else:
            image = Image.new('RGB', (64, 64), 'white')
        menu = pystray.Menu(
            pystray.MenuItem('Configurações', self._on_config, default=True),
            pystray.MenuItem('Sair', self._on_exit)
        )
        icon = pystray.Icon("open-flow", image, "Open Flow", menu)
        return icon

    def _on_config(self, icon, item):
        """Abre a janela de configurações"""
        # Garante que a UI seja manipulada na thread principal do Tk
        if self.tk_root is not None:
            self.tk_root.after(0, self.config_window.show)
        else:
            # Fallback: tenta abrir diretamente (pode falhar se não estiver na main thread)
            try:
                self.config_window.show()
            except Exception:
                pass

    def _on_exit(self, icon, item):
        # Para encerrar sem exceptions no handler do pystray, não chame sys.exit aqui.
        # Pare o tray e peça para o Tk encerrar o mainloop na thread principal.
        icon.stop()
        if self.tk_root is not None:
            try:
                self.tk_root.after(0, self.tk_root.quit)
            except Exception:
                # Como fallback extremo (não esperado neste app), evita levantar SystemExit aqui
                # para não quebrar o handler do pystray.
                pass

    def run(self):
        self.icon.run()