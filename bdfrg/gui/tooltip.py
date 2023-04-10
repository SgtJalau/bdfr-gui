import tkinter as tk


# https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
# CREDIT: squareRoot17
from bdfrg import string_utils


class Tooltip(object):

    def __init__(self, widget, text):
        self.text = text

        self.widget = widget
        self.tip_window = None
        self.id = None
        self.x = self.y = 0

        self.max_characters_per_line = 100

        # Split the text into multiple lines if it is too long
        self.formatted_text = string_utils.split_lines(text, self.max_characters_per_line)

    def showtip(self):
        """
        Display text in tooltip window
        :param text: The text to display
        :return: None
        """

        # If the tooltip window already exists or there is no text to display, do nothing
        if self.tip_window or not self.text:
            return

        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.formatted_text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        """
        Destroy the tooltip window
        :return: None
        """

        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


def create_tooltip(widget, text):
    """
    Create a tooltip for the given widget
    :param widget: The widget to create the tooltip for
    :param text: The text to display in the tooltip
    :return: The tooltip
    """
    tooltip = Tooltip(widget, text)

    def enter(event):
        """
        Show the tooltip when the mouse enters the widget
        :param event:  The event
        :return: None
        """
        tooltip.showtip()

    def leave(event):
        """
        Hide the tooltip when the mouse leaves the widget
        :param event: The event
        :return: None
        """
        tooltip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    return tooltip
