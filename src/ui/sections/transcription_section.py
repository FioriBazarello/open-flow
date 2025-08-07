import tkinter as tk
from tkinter import ttk

from src.config.options import MODEL_CHOICES, LANGUAGE_CHOICES, values, description_for


class TranscriptionSection:
    def __init__(self, parent: tk.Misc):
        self.frame = ttk.LabelFrame(parent, text="Configurações de Transcrição", padding="15")
        self.model_var = tk.StringVar()
        self.language_var = tk.StringVar()
        self._model_desc_label: ttk.Label | None = None
        self._language_desc_label: ttk.Label | None = None
        self._build()

    def _build(self) -> None:
        self.frame.columnconfigure(1, weight=1)

        ttk.Label(self.frame, text="Modelo:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        model_combo = ttk.Combobox(
            self.frame,
            textvariable=self.model_var,
            values=values(MODEL_CHOICES),
            state="readonly",
            width=20,
            font=("Arial", 10),
        )
        model_combo.grid(row=0, column=1, sticky="w", padx=(15, 0), pady=5)

        self._model_desc_label = ttk.Label(self.frame, text="", font=("Arial", 9), foreground="blue")
        self._model_desc_label.grid(row=0, column=2, sticky="w", padx=(10, 0), pady=5)

        ttk.Label(self.frame, text="Idioma:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        language_combo = ttk.Combobox(
            self.frame,
            textvariable=self.language_var,
            values=values(LANGUAGE_CHOICES),
            state="readonly",
            width=20,
            font=("Arial", 10),
        )
        language_combo.grid(row=1, column=1, sticky="w", padx=(15, 0), pady=5)

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


