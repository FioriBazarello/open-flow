import tkinter as tk
import threading
import sys

if sys.platform == 'win32':
    import winsound

class StatusIndicator:
    def __init__(self):
        self.root = tk.Tk()
        self._setup_window()
        self.state = 'inactive'

    def _setup_window(self):
        self.root.overrideredirect(True)  # Remove barra de título
        self.root.attributes('-topmost', True)  # Sempre visível
        self.root.attributes('-alpha', 1)  # Opaco
        self.root.configure(bg='black')  # Fundo preto (será transparente)

        # Para Windows: tornar o preto transparente
        if sys.platform == 'win32':
            self.root.wm_attributes('-transparentcolor', 'black')

        # Dimensões da cápsula
        margin = 20
        x_pos = margin
        y_pos = margin
        window_width = 140
        window_height = 28
        radius = window_height // 2
        capsule_color = '#222'
        border_color = '#333'
        border_width = 2

        self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # Canvas para desenhar tudo
        self.capsule_canvas = tk.Canvas(self.root, width=window_width, height=window_height, highlightthickness=0, bg='black')
        self.capsule_canvas.pack(fill='both', expand=True)

        # Desenha a borda da cápsula (formas um pouco maiores)
        self.capsule_canvas.create_oval(
            0, 0, window_height, window_height,
            fill=border_color, outline='')
        self.capsule_canvas.create_oval(
            window_width-window_height, 0, window_width, window_height,
            fill=border_color, outline='')
        self.capsule_canvas.create_rectangle(
            radius, 0, window_width-radius, window_height,
            fill=border_color, outline='')

        # Desenha a cápsula principal por cima, menor para mostrar a borda
        self.capsule_canvas.create_oval(
            border_width, border_width, window_height-border_width, window_height-border_width,
            fill=capsule_color, outline='')
        self.capsule_canvas.create_oval(
            window_width-window_height+border_width, border_width, window_width-border_width, window_height-border_width,
            fill=capsule_color, outline='')
        self.capsule_canvas.create_rectangle(
            radius, border_width, window_width-radius, window_height-border_width,
            fill=capsule_color, outline='')

        # Desenha o círculo de status encaixado na ponta esquerda
        circle_margin = 6
        circle_diam = window_height - 2*circle_margin
        self.indicator = self.capsule_canvas.create_oval(
            circle_margin, circle_margin,
            circle_margin+circle_diam, circle_margin+circle_diam,
            fill='gray', outline='')

        # Desenha o texto do estado à direita do círculo, centralizado verticalmente
        self.state_text_x = window_height + circle_margin - 6
        self.state_text_y = window_height // 2
        self.state_label = self.capsule_canvas.create_text(
            self.state_text_x, self.state_text_y,
            text='Inativo', anchor='w', fill='white', font=("Arial", 10, "bold"))

    def update_state(self, state):
        colors = {
            'inactive': 'gray',
            'recording': 'red',
            'processing': 'yellow',
            'complete': 'green'
        }
        labels = {
            'inactive': 'Inativo',
            'recording': 'Gravando...',
            'processing': 'Processando...',
            'complete': 'Concluído!'
        }
        sounds = {
            'inactive': None,
            'recording': 'start',
            'processing': 'start',
            'complete': 'complete'
        }
        if state in colors:
            def update():
                self.capsule_canvas.itemconfig(self.indicator, fill=colors[state])
                self.capsule_canvas.itemconfig(self.state_label, text=labels[state])
                self.state = state
                sound_type = sounds[state]
                if sound_type:
                    self._play_sound(sound_type)
            if threading.current_thread() is threading.main_thread():
                update()
            else:
                self.root.after(0, update)

    def _play_sound(self, sound_type):
        if sys.platform == 'win32':
            if sound_type == 'start':
                winsound.Beep(800, 120)  # frequência, duração em ms
            elif sound_type == 'stop':
                winsound.Beep(400, 120)
            elif sound_type == 'complete':
                winsound.Beep(1000, 180)
        # Para outros sistemas, pode-se usar outras libs como pygame ou simplesaudio 