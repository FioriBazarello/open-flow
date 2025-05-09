import tkinter as tk
import threading
import sys

if sys.platform == 'win32':
    import winsound

class FeedbackManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove barra de título
        self.root.attributes('-topmost', True)  # Sempre visível
        self.root.attributes('-alpha', 1)  # Semi-transparente
        self.root.configure(bg='black')  # Fundo preto
        
        # Calcula a posição para ficar no canto superior esquerdo
        margin = 20
        x_pos = margin
        y_pos = margin
        
        # Dimensões fixas para acomodar o círculo e o texto
        window_width = 120  # Largura suficiente para o texto
        window_height = 24  # Altura para alinhar círculo e texto
        
        self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        
        # Frame para manter tamanho fixo
        frame = tk.Frame(self.root, bg='black')
        frame.pack(expand=True, fill='both')
        
        # Canvas para o círculo indicador
        self.canvas = tk.Canvas(frame, width=20, height=20, highlightthickness=0, bg='black')
        self.canvas.pack(side='left', padx=(2,0))
        self.indicator = self.canvas.create_oval(2, 2, 18, 18, fill='gray')
        
        # Label para o texto do estado
        self.state_label = tk.Label(frame, text='inactive', fg='white', bg='black')
        self.state_label.pack(side='left', padx=(5,2))
        
        self.state = 'inactive'

    def update_state(self, state):
        colors = {
            'inactive': 'gray',
            'recording': 'red',
            'processing': 'yellow',
            'complete': 'green'
        }
        if state in colors:
            def update():
                self.canvas.itemconfig(self.indicator, fill=colors[state])
                self.state = state
            if threading.current_thread() is threading.main_thread():
                update()
            else:
                self.root.after(0, update)

    def play_sound(self, sound_type):
        if sys.platform == 'win32':
            if sound_type == 'start':
                winsound.Beep(800, 120)  # frequência, duração em ms
            elif sound_type == 'stop':
                winsound.Beep(400, 120)
            elif sound_type == 'complete':
                winsound.Beep(1000, 180)
        # Para outros sistemas, pode-se usar outras libs como pygame ou simplesaudio 