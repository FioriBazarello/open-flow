import tkinter as tk
from tkinter import ttk


class StatusBar:
    def __init__(self, parent: tk.Misc, *, font: tuple[str, int] = ("Arial", 9)) -> None:
        self.label = ttk.Label(parent, text="Pronto", relief=tk.SUNKEN, anchor=tk.W, font=font)

    def grid(self, **kwargs) -> None:
        self.label.grid(**kwargs)

    def set(self, message: str) -> None:
        self.label.config(text=message)


