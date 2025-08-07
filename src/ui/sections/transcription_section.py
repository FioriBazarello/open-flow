import tkinter as tk
from tkinter import ttk

from src.config.options import MODEL_CHOICES, LANGUAGE_CHOICES, values, description_for
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
            values=values(MODEL_CHOICES),
            variable=self.model_var,
            width=20,
        )
        model_field.grid(row=0, column=0, sticky="ew")

        self._model_desc_label = ttk.Label(self.frame, text="", font=("Arial", 9), foreground="blue")
        self._model_desc_label.grid(row=0, column=2, sticky="w", padx=(10, 0), pady=5)

        language_field = LabeledCombobox(
            self.frame,
            label_text="Idioma:",
            values=values(LANGUAGE_CHOICES),
            variable=self.language_var,
            width=20,
        )
        language_field.grid(row=1, column=0, sticky="ew")

        self._language_desc_label = ttk.Label(self.frame, text="", font=("Arial", 9), foreground="blue")
        self._language_desc_label.grid(row=1, column=2, sticky="w", padx=(10, 0), pady=5)

        self.model_var.trace_add("write", lambda *_: self._sync_descriptions())
        self.language_var.trace_add("write", lambda *_: self._sync_descriptions())

    def grid(self, **kwargs) -> None:
        self.frame.grid(**kwargs)

    def load(self, model_name: str, language: str) -> None:
        self.model_var.set(model_name)
        self.language_var.set(language)
        self._sync_descriptions()

    def values(self) -> dict:
        return {"model_name": self.model_var.get(), "language": self.language_var.get()}

    def _sync_descriptions(self) -> None:
        if self._model_desc_label is not None:
            self._model_desc_label.config(text=description_for(MODEL_CHOICES, self.model_var.get()) or "")
        if self._language_desc_label is not None:
            self._language_desc_label.config(text=description_for(LANGUAGE_CHOICES, self.language_var.get()) or "")


