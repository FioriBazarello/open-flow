import tkinter as tk
from tkinter import ttk

from src.ui.components import LabeledEntry, FormSection


class GeneralSection(FormSection):
    def __init__(self, parent: tk.Misc):
        super().__init__(parent, title="Configurações Gerais", padding="15")
        self.ollama_field: LabeledEntry | None = None
        self._build()

    def _build(self) -> None:
        self.frame.columnconfigure(0, weight=1)
        self.ollama_field = LabeledEntry(self.frame, label_text="Servidor Ollama:", width=50)
        self.ollama_field.grid(row=0, column=0, sticky="ew")

    def grid(self, **kwargs) -> None:
        self.frame.grid(**kwargs)

    def load(self, ollama_base_url: str) -> None:
        if self.ollama_field is not None:
            self.ollama_field.set_value(ollama_base_url)

    def values(self) -> dict:
        return {"ollama_base_url": self.ollama_field.get_value() if self.ollama_field else ""}


