import tkinter as tk

from default_entry import DefaultEntry

def is_showing_default(widget: tk.Widget):
    # Check if it is a DefaultEntry
    if isinstance(widget, DefaultEntry):
        return widget.is_showing_default()

    return False
