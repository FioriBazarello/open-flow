import tkinter as tk
from tkinter import ttk
from typing import Iterable


class LabeledCombobox:
    def __init__(
        self,
        parent: tk.Misc,
        label_text: str,
        values: Iterable[str] | None = None,
        variable: tk.StringVar | None = None,
        *,
        width: int = 20,
        font: tuple[str, int, str] | tuple[str, int] = ("Arial", 10),
        state: str = "readonly",
    ) -> None:
        self.container = ttk.Frame(parent)
        self.label = ttk.Label(self.container, text=label_text, font=("Arial", 10, "bold"))
        self.variable = variable or tk.StringVar()
        self.combobox = ttk.Combobox(
            self.container,
            textvariable=self.variable,
            values=list(values) if values is not None else [],
            state=state,
            width=width,
            font=font,
        )

        self.container.columnconfigure(1, weight=1)
        self.label.grid(row=0, column=0, sticky="w", pady=5)
        self.combobox.grid(row=0, column=1, sticky="ew", padx=(15, 0), pady=5)

    def grid(self, **kwargs) -> None:
        self.container.grid(**kwargs)

    def set_values(self, values: Iterable[str]) -> None:
        self.combobox["values"] = list(values)

    def set_value(self, value: str) -> None:
        self.variable.set(value)

    def get_value(self) -> str:
        return self.variable.get()

    def focus(self) -> None:
        self.combobox.focus_set()


