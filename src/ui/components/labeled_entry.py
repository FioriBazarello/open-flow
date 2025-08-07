import tkinter as tk
from tkinter import ttk


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
        self.entry = ttk.Entry(self.container, width=width, font=font, show=show)

        self.container.columnconfigure(1, weight=1)
        self.label.grid(row=0, column=0, sticky="w", pady=5)
        self.entry.grid(row=0, column=1, sticky="ew", padx=(15, 0), pady=5)

    def grid(self, **kwargs) -> None:
        self.container.grid(**kwargs)

    def set_value(self, value: str) -> None:
        self.entry.delete(0, "end")
        self.entry.insert(0, value)

    def get_value(self) -> str:
        return self.entry.get()

    def focus(self) -> None:
        self.entry.focus_set()


