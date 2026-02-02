import os.path

from connection import Connection
from PyQt6.QtWidgets import QStyleFactory

def getCurrentStyle():
    """
    Retrieves the currently active theme name from the application settings in the database.

    :return: The name of the theme (e.g., 'Dark', 'Light').
    :rtype: str
    """
    all_data_settings = Connection.getSettings()
    for key, value in all_data_settings:
        if key == 'theme':
            return value
    return "Dark"


def load_stylesheet():
    """
    Reads the content of the .qss file corresponding to the current theme.

    :return: The raw CSS/QSS string.
    :rtype: str
    """
    with open(f"styles/{getCurrentStyle()}.qss") as file:
        return file.read()

def get_all_styles():
    """
     Scans the 'styles' directory and returns a list of all available theme names.

    :return: A list of theme names without file extensions.
    :rtype: list
    """
    styles_path = "styles"
    if not os.path.exists(styles_path):
        return []

    return [os.path.splitext(f)[0] for f in os.listdir(styles_path) if f.endswith(".qss")]