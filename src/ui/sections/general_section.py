import tkinter as tk
from tkinter import ttk


class GeneralSection:
    def __init__(self, parent: tk.Misc):
        self.frame = ttk.LabelFrame(parent, text="Configurações Gerais", padding="15")
        self.ollama_entry: ttk.Entry | None = None
        self._build()

    def _build(self) -> None:
        self.frame.columnconfigure(1, weight=1)
        ttk.Label(self.frame, text="Servidor Ollama:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.ollama_entry = ttk.Entry(self.frame, width=50, font=("Arial", 10))
        self.ollama_entry.grid(row=0, column=1, sticky="ew", padx=(15, 0), pady=5)

    def grid(self, **kwargs) -> None:
        self.frame.grid(**kwargs)

    def load(self, ollama_base_url: str) -> None:
        if self.ollama_entry is None:
            return
        self.ollama_entry.delete(0, "end")
        self.ollama_entry.insert(0, ollama_base_url)

    def values(self) -> dict:
        return {"ollama_base_url": self.ollama_entry.get() if self.ollama_entry else ""}


