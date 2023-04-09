import tkinter as tk


class DefaultEntry(tk.Entry):
    """
    A custom Tkinter Entry widget that allows for a default value to be shown, that disappears once the user clicks
    into it.

    :param master: The parent widget.
    :type master: tk.Widget
    :param default_text: The default text to show in the widget.
    :type default_text: str
    :param default_color: The color of the default text. Default is 'grey'.
    :type default_color: str
    """

    def __init__(self, master=None, default_text='', default_color='grey', **kwargs):
        super().__init__(master=master, **kwargs)
        self.default_text = default_text
        self.default_color = default_color

        # Check if self has no text to make sure we don't overwrite or append to in the constructor passed default text
        if not self.get():
            self.insert(0, default_text)
            self.config(fg=default_color)

        self.bind('<FocusIn>', self.on_click)
        self.bind('<FocusOut>', self.on_blur)

    def set_default_text(self, default_text):
        """
        Set the default text to show in the widget.

        :param default_text: The new default text.
        :type default_text: str
        """
        self.default_text = default_text

    def on_click(self, event):
        """
        Event handler for when the widget gains focus.
        """
        if self.get() == self.default_text:
            self.delete(0, tk.END)
            self.config(fg='black')

    def on_blur(self, event):
        """
        Event handler for when the widget loses focus.
        """
        if not self.get():
            self.insert(0, self.default_text)
            self.config(fg=self.default_color)

    def has_focus(self):
        """
        Check if the widget currently has focus.

        :return: True if the widget has focus, False otherwise.
        :rtype: bool
        """
        return self.focus_get() == self

    def is_showing_default(self):
        """
        Check if the widget is currently showing the default text.

        :return: True if the widget is showing the default text, False otherwise.
        :rtype: bool
        """
        return not self.has_focus()
