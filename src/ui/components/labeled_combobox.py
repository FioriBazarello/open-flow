import tkinter as tk
from tkinter import ttk
from typing import Iterable, Any


class LabeledCombobox:
    def __init__(
        self,
        parent: tk.Misc,
        label_text: str,
        *,
        values: Iterable[str] | None = None,
        choices: Iterable[object] | None = None,
        variable: tk.StringVar | None = None,
        width: int = 20,
        font: tuple[str, int, str] | tuple[str, int] = ("Arial", 10),
        state: str = "readonly",
    ) -> None:
        self.container = ttk.Frame(parent)
        self.label = ttk.Label(self.container, text=label_text, font=("Arial", 10, "bold"))

        # External variable stores the VALUE; internal display variable stores the LABEL
        self.variable = variable or tk.StringVar()
        self._display_var = tk.StringVar()

        # Mappings between labels and values
        self._value_for_label: dict[str, str] = {}
        self._label_for_value: dict[str, str] = {}

        self.combobox = ttk.Combobox(
            self.container,
            textvariable=self._display_var,
            values=[],
            state=state,
            width=width,
            font=font,
        )

        self.container.columnconfigure(0, weight=1)
        self.label.grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.combobox.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        # Reentrancy guards
        self._updating_from_value = False
        self._updating_from_display = False

        # Initialize choices/values
        if choices is not None:
            self.set_choices(choices)
        elif values is not None:
            self.set_values(values)

        # Sync when user selects a label
        self.combobox.bind("<<ComboboxSelected>>", lambda _e: self._on_display_changed())
        self._display_var.trace_add("write", lambda *_: self._on_display_changed())

        # Sync when external value variable changes
        self.variable.trace_add("write", lambda *_: self._on_value_changed())

        # Initial sync
        self._on_value_changed()

    def grid(self, **kwargs) -> None:
        self.container.grid(**kwargs)

    def set_values(self, values: Iterable[str]) -> None:
        labels = list(values)
        # Identity mapping when only raw values provided
        self._value_for_label = {label: label for label in labels}
        self._label_for_value = {label: label for label in labels}
        self.combobox["values"] = labels

    def set_value(self, value: str) -> None:
        self.variable.set(value)

    def get_value(self) -> str:
        return self.variable.get()

    def focus(self) -> None:
        self.combobox.focus_set()

    def set_choices(self, choices: Iterable[object]) -> None:
        labels: list[str] = []
        value_for_label: dict[str, str] = {}
        label_for_value: dict[str, str] = {}
        for c in choices:
            # tolerate duck-typed objects
            label = getattr(c, "label", None)
            value = getattr(c, "value", None)
            if not isinstance(label, str) or not isinstance(value, str):
                continue
            labels.append(label)
            value_for_label[label] = value
            label_for_value[value] = label
        self._value_for_label = value_for_label
        self._label_for_value = label_for_value
        self.combobox["values"] = labels
        # Refresh display according to current value
        self._on_value_changed()

    def _on_display_changed(self) -> None:
        if self._updating_from_value:
            return
        self._updating_from_display = True
        try:
            label = self._display_var.get()
            value = self._value_for_label.get(label, label)
            if self.variable.get() != value:
                self.variable.set(value)
        finally:
            self._updating_from_display = False

    def _on_value_changed(self) -> None:
        if self._updating_from_display:
            return
        self._updating_from_value = True
        try:
            value = self.variable.get()
            label = self._label_for_value.get(value, value)
            if self._display_var.get() != label:
                self._display_var.set(label)
        finally:
            self._updating_from_value = False


