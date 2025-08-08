import tkinter as tk
from tkinter import ttk

from src.config.options import MODEL_CHOICES, LANGUAGE_CHOICES
from src.ui.components import LabeledCombobox, FormSection


class TranscriptionSection(FormSection):
    def __init__(self, parent: tk.Misc):
        super().__init__(parent, title="Configurações de Transcrição", padding="15")
        self.model_var = tk.StringVar()
        self.language_var = tk.StringVar()
        self._model_desc_label: ttk.Label | None = None
        self._language_desc_label: ttk.Label | None = None
        self._build()

    def _build(self) -> None:
        self.frame.columnconfigure(0, weight=1)

        model_field = LabeledCombobox(
            self.frame,
            label_text="Modelo:",
            choices=MODEL_CHOICES,
            variable=self.model_var,
            width=20,
        )
        model_field.grid(row=0, column=0, sticky="ew")

        language_field = LabeledCombobox(
            self.frame,
            label_text="Idioma:",
            choices=LANGUAGE_CHOICES,
            variable=self.language_var,
            width=20,
        )
        language_field.grid(row=1, column=0, sticky="ew")
        
        # Não há mais descrições separadas; labels já incluem informação

    def grid(self, **kwargs) -> None:
        self.frame.grid(**kwargs)

    def load(self, model_name: str, language: str) -> None:
        self.model_var.set(model_name)
        self.language_var.set(language)
        self._sync_descriptions()

    def values(self) -> dict:
        return {"model_name": self.model_var.get(), "language": self.language_var.get()}

    def _sync_descriptions(self) -> None:
        # Método mantido por compatibilidade, mas não faz nada agora
        pass


