import json
import os
import tkinter as tk
from dataclasses import fields
from enum import Enum
from tkinter import messagebox
from typing import List

import tkinter_utils
from bdfrg import type_utils
from bdfrg.input_configuration import InputConfiguration, serialize_input_configuration
from bdfrg.reddit import reddit_utils
from bdfrg.reddit.reddit_utils import RedditUrlType
from default_entry import DefaultEntry
from tooltip import create_tooltip

current_directory_path = os.path.dirname(os.path.realpath(__file__))

field_formatting = {}

fields_folder = os.path.join(os.path.join(current_directory_path, 'fields'))

# Load tooltips from directory (gui/tooltips)
for file in os.listdir(fields_folder):
    # Only txt files
    if file.endswith('.json'):
        with open(os.path.join(fields_folder, file)) as f:
            # Load json
            field_format = json.load(f)
            field_formatting[field_format['name']] = field_format


class VariableWrapper:
    """
    A wrapper class for Tkinter variables that provides additional functionality.

    :param variable: The Tkinter variable to wrap.
    :type variable: tk.Variable
    :param field_name: The name of the field that this variable represents.
    :type field_name: str
    :param parent_object: The object that owns this variable.
    :param widget: The widget that this variable is associated with.
    :type widget: tk.Widget
    """

    def __init__(self, variable: tk.Variable, field_name: str, parent_object, widget: tk.Widget):
        self.variable = variable
        self.field_name = field_name
        self.parent_object = parent_object
        self.widget: tk.Widget = widget

    def get(self):
        """
        Get the value of the wrapped variable.

        :return: The value of the wrapped variable.
        """
        # If float or int and empty, return 0
        if self.variable.get() == '' and (type(self.variable) == tk.DoubleVar or type(self.variable) == tk.IntVar):
            return 0
        return self.variable.get()


def validate_input(new_text: str, old_text: str, field_type: type, widget: tk.Widget) -> bool:
    """
    Validate new input for a field.

    :param new_text: The new text to validate.
    :type new_text: str
    :param old_text: The old text in the field.
    :type old_text: str
    :param field_type: The type of the field (int or float).
    :type field_type: type
    :param widget: The widget that the input is being validated for.
    :type widget: tk.Widget
    :return: True if the input is valid, False otherwise.
    """
    if field_type == int:
        # Check if the new text is a digit, or if it is empty, we need to allow default placeholder text
        if not tkinter_utils.is_showing_default(widget) and not new_text.isdigit() and new_text != '':
            return False
    elif field_type == float:
        # Check if the new text is a digit, or if it is empty,
        # we need to allow default placeholder text and a decimal point
        if not tkinter_utils.is_showing_default(widget) and not new_text.replace('.', '',
                                                                                 1).isdigit() and new_text != '':
            return False

    return True


def field_name_to_label_name(field_name: str) -> str:
    """
    Convert a field name to a label name. This is done by replacing underscores with spaces and capitalizing the first letter.

    :param field_name: The name of the field.
    :type field_name: str
    :return: The label name for the given field name.
    """
    return field_name.replace('_', ' ').capitalize()


class ConfigurationGUI(tk.Frame):

    def __init__(self, master=None, input_configuration: InputConfiguration = InputConfiguration()):
        super().__init__(master)
        self.master = master
        self.input_configuration = input_configuration
        # Stores the field variables by field_var name (e.g PYVAR1 -> VariableWrapper)
        self.variables: dict = {}
        self.serialized_config = None
        self.popup = None

        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Set padding bottom
        self.grid(pady=10)

        # Set padding left and right
        self.grid(padx=10)

        # Create widgets

        self.create_widgets()

    def get_widget_by_name(self, widget_name: str) -> tk.Widget:
        """
        Get a widget by its name.
        :param widget_name: The name of the widget to get (e.g. 'myframe.mybutton').
        :return: The widget with the given name.
        """
        return self.nametowidget(widget_name)

    def get_variable_for_configuration_field(self, field_name: str) -> VariableWrapper:
        for pyvar, variable_wrapper in self.variables.items():
            if variable_wrapper.field_name == field_name:
                return variable_wrapper

    # We need this intermediate function because the validate command only passes through strings, not the actual field type
    def validate_integer(self, new_text: str, old_text: str, widget_name: str) -> bool:
        """
        Validate new input for an integer field.

        :param new_text: The new text to validate.
        :type new_text: str
        :param old_text: The old text in the field.
        :type old_text: str
        :param widget_name: The name of the widget that the input is being validated for.
        :type widget_name: str
        :return: True if the input is valid, False otherwise.
        """

        return validate_input(new_text, old_text, int, self.get_widget_by_name(widget_name))

    def validate_float(self, new_text: str, old_text: str, widget_name: str) -> bool:
        """
        Validate new input for a float field. This is done by checking if the new text is a digit, or if it is empty, we need to

        :param new_text: The new text to validate.
        :type new_text: str
        :param old_text: The old text in the field.
        :type old_text: str
        :param widget_name: The name of the widget that the input is being validated for.
        :type widget_name: str
        :return: True if the input is valid, False otherwise.
        """
        return validate_input(new_text, old_text, float, self.get_widget_by_name(widget_name))

    def on_var_write_trace(self, *args):
        """
        This function is called when a variable is written to. It updates the configuration dataclass with the new value.
        :param args: The arguments passed by the trace function. (0: The name of the variable that was changed)
        :return: None
        """
        # Get the variable that was changed
        variable: str = args[0]

        # Get the field name (of the configuration dataclass) of the variable
        variable: VariableWrapper = self.variables[variable]

        # Ignore if the variable is a DefaultEntry and is showing the default value
        if isinstance(variable.widget, DefaultEntry) and variable.widget.is_showing_default():
            return

        self.set_configuration_value_and_update(variable.parent_object, variable.field_name, variable.get())

    def create_grid_section(self, headline, column):
        # Create a new grid in the first column
        grid = tk.Frame(self, highlightbackground="#ded9d9", highlightthickness=2)
        # Give it two columns
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        # Place it in the first column
        grid.grid(row=0, column=column, sticky=tk.N + tk.S + tk.E + tk.W)

        # Create headline label
        headline = tk.Label(grid, text=headline)
        headline.config(font=('Arial', 15), bg='#ded9d9')
        headline.grid(row=0, column=0, rowspan=3, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        # Set padding right and left
        grid.columnconfigure(0, pad=10)
        grid.columnconfigure(1, pad=10)

        return grid

    def create_widgets(self):
        grid = self.create_grid_section('Input Configuration', 0)

        # Create widgets for the input configuration
        row, column = self.create_widgets_for_class(grid, self.input_configuration, 4, 0)

        grid = self.create_grid_section('Downloader Configuration', 1)

        # Create widgets for downloader configuration
        row, column = self.create_widgets_for_class(grid, self.input_configuration.download_config, 4, 0)

        grid = self.create_grid_section('Archiver Configuration', 2)

        # Create widgets for archiver configuration
        row, column = self.create_widgets_for_class(grid, self.input_configuration.archiver_config, 4, 0)

        # Create headline label
        headline = tk.Label(self, text='Output Preview')
        headline.config(font=('Arial', 15), bg='#ded9d9')
        headline.grid(row=1, column=0, rowspan=3, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

        # Add the serialized configuration to the gui as a textbonx on the right
        self.serialized_config = serialized_config = tk.Text(self)
        serialized_config.config(height=10, width=50)
        serialized_config.grid(row=5, column=0, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
        serialized_config.insert(tk.END, serialize_input_configuration(self.input_configuration))

        # Bottom padding before toolbar
        self.rowconfigure(6, pad=10)

        add_button = tk.Button(self, text="+", fg="green", command=self.on_add_link_press)
        # Font size for +
        add_button.config(font=('Arial', 20))
        add_button.grid(row=6, column=0, sticky=tk.W)

    def on_add_link_press(self):
        self.popup = tk.Toplevel()
        self.popup.title("Add URL")

        url_label = tk.Label(self.popup, text="URL:")
        url_label.pack(side=tk.LEFT)

        url_entry = tk.Entry(self.popup)
        url_entry.pack(side=tk.LEFT)

        add_button = tk.Button(self.popup, text="Add", command=lambda: self.on_input_url(url_entry.get()))
        add_button.pack(side=tk.LEFT)

    def close_add_url_popup(self):
        # Close popup
        self.popup.destroy()
        self.popup.update()

    def on_input_url(self, url):
        # Do something with the link
        print(f"URL added: {url}")

        try:
            url_type = reddit_utils.get_reddit_type_from_url(url)
            self.add_url(url, url_type)
            self.close_add_url_popup()
        except Exception as e:
            messagebox.showerror("Error", e)

    def add_url(self, url: str, url_type: RedditUrlType):
        try:
            identifying_part = reddit_utils.get_identifying_part_of_reddit_url(url, url_type)

            if url_type is RedditUrlType.SUBREDDIT:
                # Append identifying part to widget
                variable_wrapper: VariableWrapper = self.get_variable_for_configuration_field('subreddit')
            elif url_type is RedditUrlType.MULTIREDDIT:
                # Append identifying part to widget
                variable_wrapper: VariableWrapper = self.get_variable_for_configuration_field('multireddit')
            elif url_type is RedditUrlType.USER:
                # Append identifying part to widget
                variable_wrapper: VariableWrapper = self.get_variable_for_configuration_field('user')
            elif url_type is RedditUrlType.POST or url_type is RedditUrlType.COMMENT:
                # Append identifying part to widget
                variable_wrapper: VariableWrapper = self.get_variable_for_configuration_field('link')
            else:
                raise Exception('Unsupported URL')

            to_insert = identifying_part

            var_val = variable_wrapper.variable.get()

            # If empty, no new line at the start, but otherwise if we aren't in a blank new line append new line before new link
            # None because the var is 'None' if initialized by None python type
            if len(var_val) != 0 and var_val != 'None' and not var_val.endswith('\n'):
                to_insert = '\n' + to_insert

            # Add new row to the widget (tk.Text or tk.Entry)
            variable_wrapper.widget.insert(tk.END, to_insert)
            variable_wrapper.variable.set(identifying_part)

            self.update_serialized_command_preview()
        except Exception as e:
            messagebox.showerror("Error", e)


    def create_widgets_for_class(self, parent, instance, start_row, start_column):
        row = start_row
        column = start_column

        field_types = {field.name: field.type for field in fields(type(instance))}

        # Grouped by type
        grouped_fields = {}

        # Go over all fields in the input configuration and create a widget for each one
        for field in instance.__dict__:
            field_type = field_types[field]
            (label, field_widget, field_var) = self.create_widget_for_field(parent, field, field_type, instance)

            if field_widget is None:
                print(f'Could not create widget for field {field}')
                continue

            # Group the fields by type
            if field_type not in grouped_fields:
                grouped_fields[field_type] = []

            grouped_fields[field_type].append((label, field_widget, field_var))

        # Go over the grouped fields and add them to the gui
        for field_type, field_list in grouped_fields.items():
            for touple in field_list:
                (label, field_widget, field_var) = touple

                # Add the label to the grid
                label.grid(row=row, column=column)
                row += 1

                # Add the field widget to the grid
                field_widget.grid(row=row, column=column)
                row += 1

                if row >= 30:
                    row = start_row
                    column += 1

        return row, column

    def create_widget_for_field(self, parent, field_name, type_val, instance):
        # Create a label
        label = tk.Label(parent, text=field_name_to_label_name(field_name))

        # Variable bound to the field
        field_var = None

        field_widget = None

        # Check type of field
        if type_val == bool:
            # Create a variable bound to the field
            field_var = boolean_var = tk.BooleanVar()
            boolean_var.set(instance.__dict__[field_name])

            # Create a checkbox
            field_widget = tk.Checkbutton(parent, variable=boolean_var)
        elif type_val == str:
            # Create a variable bound to the field
            field_var = tk.StringVar()
            # if the field is None, set it to an empty string (otherwise the text box will show 'None')
            field_var.set(instance.__dict__[field_name] if instance.__dict__[field_name] else '')

            # Check if field name is in value_suggestions
            if field_name in field_formatting and 'suggestion' in field_formatting[field_name]:
                # Create a text box with a default value
                field_widget = DefaultEntry(parent, textvariable=field_var,
                                            default_text=field_formatting[field_name]['suggestion'])
            else:
                # Create a text box
                field_widget = tk.Entry(parent, textvariable=field_var)

            # Make it wider
            field_widget.config(width=50)
        elif type_val == int:
            # Create a variable bound to the field
            field_var = tk.StringVar()

            # Set the variable to the value of the field,
            # if the field is None, set it to an empty string (otherwise the text box will show 'None')
            field_var.set(instance.__dict__[field_name] if instance.__dict__[field_name] else '')

            # Create a text box that only accepts integers
            field_widget = DefaultEntry(parent, textvariable=field_var, default_text='e.g. 123', default_color='grey')

            # Make it only accept integers using the validate_input function as a callback for the text box
            validate_input_callback = (parent.register(self.validate_integer))
            field_widget.config(validate='key', validatecommand=(validate_input_callback, '%P', '%S', '%W'))
        elif type_val == List[str]:
            # Create a variable bound to the field
            field_var = list_var = tk.StringVar()
            list_var.set(instance.__dict__[field_name])

            # Create a text box that accepts multiple lines
            field_widget = tk.Text(parent)

            # Set width of widget
            field_widget.config(width=50)

            # On change of the text box, update the variable
            field_widget.bind('<KeyRelease>', lambda event: list_var.set(field_widget.get('1.0', tk.END)))

            # Rows shown default 3
            field_widget.config(height=3)
        elif issubclass(type_val, Enum):
            # Create a variable bound to the field
            field_var = time_filter_var = tk.StringVar()
            time_filter_var.set(instance.__dict__[field_name].name)

            # All enum values without the current selected
            options = [str(x.name) for x in type_val if x.name != instance.__dict__[field_name].name]

            # Create a dropdown menu with the names of the enum values
            field_widget = tk.OptionMenu(parent, time_filter_var, instance.__dict__[field_name].name,
                                         *options)
        elif type_val == float:
            # Create a variable bound to the field
            field_var = tk.StringVar()

            # Set the variable to the value of the field,
            # if the field is None, set it to an empty string (otherwise the text box will show 'None')
            field_var.set(instance.__dict__[field_name] if instance.__dict__[field_name] else '')

            # Create a text box that only accepts floats
            field_widget = DefaultEntry(parent, textvariable=field_var, default_text='e.g. 1.0', default_color='grey')

            # Make it only accept floats using the validate_input function as a callback for the text box
            validate_input_callback = (parent.register(self.validate_float))
            field_widget.config(validate='key', validatecommand=(validate_input_callback, '%P', '%S', '%W'))

        # If we created a variable, bind it to the field
        if field_var:
            # Trace write to setter of data class for field
            field_var.trace_add('write', self.on_var_write_trace)

            name = field_var._name

            # Track variables because of garbage collection and we need to find it in the trace callback
            self.variables[name] = VariableWrapper(field_var, field_name, instance, field_widget)
        if field_widget and field_name in field_formatting and 'tooltip' in field_formatting[field_name]:
            # Create a tooltip
            create_tooltip(field_widget, field_formatting[field_name]['tooltip'])

        return label, field_widget, field_var

    def set_configuration_value_and_update(self, configuration, field: str, value):
        field_types = type_utils.get_field_types_of_dataclass(type(configuration))
        field_type = field_types[field]

        # If the value is a string, convert it to the correct type
        if type(value) == str:
            # Convert the value to the correct type
            value = type_utils.convert_str_to_type(value, field_type)

        # Set the field to the new value
        setattr(configuration, field, value)
        self.update_serialized_command_preview()

    def update_serialized_command_preview(self):
        """
        Updates the serialized command preview widget with the current text
        :return: None
        """
        # Update the serialized configuration (delete and reinsert)
        self.serialized_config.delete(1.0, tk.END)
        self.serialized_config.insert(tk.END, serialize_input_configuration(self.input_configuration))


# Create an open gui
root = tk.Tk()
# Set name of window
root.title('Bulk Downloader For Reddit GUI')


app = ConfigurationGUI(master=root)
app.mainloop()
