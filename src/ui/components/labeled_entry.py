import tkinter as tk
from tkinter import ttk
from typing import Any


class LabeledEntry:
    def __init__(
        self,
        parent: tk.Misc,
        label_text: str,
        *,
        width: int = 50,
        font: tuple[str, int, str] | tuple[str, int] = ("Arial", 10),
        show: str | None = None,
    ) -> None:
        self.container = ttk.Frame(parent)
        self.label = ttk.Label(self.container, text=label_text, font=("Arial", 10, "bold"))
        entry_kwargs: dict[str, Any] = {"width": width, "font": font}
        if show is not None:
            entry_kwargs["show"] = show
        self.entry = ttk.Entry(self.container, **entry_kwargs)

        # Layout vertical (label acima do campo), alinhado ao comportamento do LabeledCombobox
        self.container.columnconfigure(0, weight=1)
        self.label.grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.entry.grid(row=1, column=0, sticky="ew", pady=(0, 5))

    def grid(self, **kwargs) -> None:
        self.container.grid(**kwargs)

    def set_value(self, value: str) -> None:
        self.entry.delete(0, "end")
        self.entry.insert(0, value)

    def get_value(self) -> str:
        return self.entry.get()

    def focus(self) -> None:
        self.entry.focus_set()


