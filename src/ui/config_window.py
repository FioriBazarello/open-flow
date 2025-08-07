import tkinter as tk
from tkinter import ttk

from src.config.settings import Settings
from src.ui.sections.transcription_section import TranscriptionSection
from src.ui.sections.general_section import GeneralSection


class ConfigWindow:
    def __init__(self, master: tk.Misc | None = None):
        self._master = master
        self._hidden_root: tk.Tk | None = None
        self._window: tk.Toplevel | None = None
        self._status_label: ttk.Label | None = None
        self._transcription_section: TranscriptionSection | None = None
        self._general_section: GeneralSection | None = None

    # Backwards compatibility with previous API
    def create_window(self) -> None:
        self.show()

    def show(self) -> None:
        # Reutiliza janela existente
        if self._window is not None and self._window.winfo_exists():
            self._window.deiconify()
            self._window.lift()
            self._window.focus_force()
            return

        # Garante uma raiz Tk quando nenhum master foi fornecido
        if self._master is None:
            self._hidden_root = tk.Tk()
            self._hidden_root.withdraw()
            master = self._hidden_root
        else:
            master = self._master

        self._window = tk.Toplevel(master)
        self._window.title("Open Flow - Configurações")
        self._window.geometry("700x550")
        self._window.resizable(True, True)
        self._window.protocol("WM_DELETE_WINDOW", self._on_close)

        # Centraliza
        self._window.update_idletasks()
        x = (self._window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self._window.winfo_screenheight() // 2) - (550 // 2)
        self._window.geometry(f"700x550+{x}+{y}")

        self._build_content(self._window)
        self._load()

    def _build_content(self, root: tk.Misc) -> None:
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        if isinstance(root, (tk.Tk, tk.Toplevel)):
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)

        ttk.Label(main_frame, text="Configurações do Open Flow", font=("Arial", 16, "bold")).grid(
            row=0, column=0, pady=(0, 20), sticky="w"
        )

        self._transcription_section = TranscriptionSection(main_frame)
        self._transcription_section.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        self._general_section = GeneralSection(main_frame)
        self._general_section.grid(row=2, column=0, sticky="ew")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(20, 0), sticky="e")
        ttk.Button(button_frame, text="Salvar Configurações", command=self._save).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancelar", command=self._on_close).pack(side=tk.LEFT)

        self._status_label = ttk.Label(main_frame, text="Pronto", relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 9))
        self._status_label.grid(row=4, column=0, sticky="ew", pady=(15, 0))

    def _load(self) -> None:
        if self._transcription_section is not None:
            self._transcription_section.load(Settings.get_model_name(), Settings.get_language())
        if self._general_section is not None:
            self._general_section.load(Settings.get_ollama_base_url())
        self._status("Configurações carregadas com sucesso")

    def _save(self) -> None:
        vals: dict = {}
        if self._transcription_section is not None:
            vals.update(self._transcription_section.values())
        if self._general_section is not None:
            vals.update(self._general_section.values())

        if "model_name" in vals:
            Settings.set_model_name(vals["model_name"])  # noqa: FBT003
        if "language" in vals:
            Settings.set_language(vals["language"])  # noqa: FBT003
        if "ollama_base_url" in vals and vals["ollama_base_url"]:
            Settings.set_ollama_base_url(vals["ollama_base_url"])  # noqa: FBT003

        self._status("Configurações salvas com sucesso!")
        self._on_close()

    def _status(self, message: str) -> None:
        if self._status_label is not None:
            self._status_label.config(text=message)

    def _on_close(self) -> None:
        if self._window is not None:
            self._window.destroy()
            self._window = None
        if self._hidden_root is not None:
            # Fecha a raiz oculta para não manter o processo preso
            try:
                self._hidden_root.destroy()
            finally:
                self._hidden_root = None
