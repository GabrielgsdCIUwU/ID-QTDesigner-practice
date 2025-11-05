import os.path

from connection import Connection
from PyQt6.QtWidgets import QStyleFactory

def getCurrentStyle():

    all_data_settings = Connection.getSettings()
    for key, value in all_data_settings:
        if key == 'theme':
            return value
    return "Dark"


def load_stylesheet():
    with open(f"styles/{getCurrentStyle()}.qss") as file:
        return file.read()

def get_all_styles():
    styles_path = "styles"
    if not os.path.exists(styles_path):
        return []

    return [os.path.splitext(f)[0] for f in os.listdir(styles_path) if f.endswith(".qss")]