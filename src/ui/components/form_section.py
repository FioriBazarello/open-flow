import tkinter as tk
from tkinter import ttk


class FormSection:
    def __init__(self, parent: tk.Misc, *, title: str, padding: str | int = "15") -> None:
        self.frame = ttk.LabelFrame(parent, text=title, padding=padding)

    def grid(self, **kwargs) -> None:
        self.frame.grid(**kwargs)


