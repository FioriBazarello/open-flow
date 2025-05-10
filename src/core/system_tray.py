import pystray
from PIL import Image
import os

class SystemTray:
    def __init__(self, icon_path=None):
        self.icon_path = icon_path
        self.icon = self._create_icon()

    def _create_icon(self):
        if self.icon_path and os.path.exists(self.icon_path):
            image = Image.open(self.icon_path)
            image = image.resize((64, 64), Image.Resampling.LANCZOS)
        else:
            image = Image.new('RGB', (64, 64), 'white')
        menu = pystray.Menu(
            pystray.MenuItem('Sair', self._on_exit)
        )
        return pystray.Icon("open-flow", image, "Open Flow", menu)

    def _on_exit(self, icon, item):
        icon.stop()
        os._exit(0)

    def run(self):
        self.icon.run()