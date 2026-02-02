from PyQt6.uic.Compiler.qtproxies import QtWidgets

import globals
import events
import styles
from dlgCalendar import *
from dlgAbout import *
from dlgSettings import *
from datetime import  datetime
from connection import Connection

from events import Events


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        """
        Initializes the calendar dialog, setting the default selection to today's date.
        """
        super(Calendar, self).__init__()
        globals.vencal = Ui_dlgCalendar()
        globals.vencal.setupUi(self)
        self.setStyleSheet(styles.load_stylesheet())
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        globals.vencal.Calendar.setSelectedDate((QtCore.QDate(year, month, day)))
        globals.vencal.Calendar.clicked.connect(events.Events.loadData)

class About(QtWidgets.QDialog):
    def __init__(self):
        """
        Initializes the 'About' dialog and sets up the close button functionality.
        """
        super(About, self).__init__()
        globals.about = Ui_dlgAbout()
        globals.about.setupUi(self)
        globals.about.btn_close_about.clicked.connect(lambda: globals.about.hide())
        self.setStyleSheet(styles.load_stylesheet())


class FileDialog(QtWidgets.QFileDialog):
    def __init__(self):
        """
        Initializes the standard system file dialog for open/save operations.
        """
        super(FileDialog, self).__init__()

class Settings(QtWidgets.QDialog):
    def __init__(self):
        """
        Initializes the settings dialog, loading available themes and applying the current stylesheet.
        """
        super(Settings, self).__init__()
        globals.settings_ui = Ui_settings()
        globals.settings_ui.setupUi(self)
        globals.settings_ui.btn_cancel_settings.clicked.connect(lambda: globals.settings.hide())
        globals.settings_ui.btn_save_settings.clicked.connect(lambda: Events.saveSettings())
        self.setStyleSheet(styles.load_stylesheet())

        self.loadAllStyles()

    @staticmethod
    def loadSettings():
        """
        Retrieves application settings from the database. Creates default values if the table is empty.

        :return: List of tuples (key, value) representing application settings.
        :rtype: list
        """
        if not Connection.getSettings():
            data = [("theme", "Dark")]
            if not Connection.saveSettings(data):
                print("Error while saving the settings")

        return Connection.getSettings()


    @staticmethod
    def loadAllStyles():
        """
        Populates the theme selection combo box with all .qss files found in the styles directory.
        """
        globals.settings_ui.cb_themes.clear()
        globals.settings_ui.cb_themes.addItems(styles.get_all_styles())

    @staticmethod
    def displayCurrentSettings(data):
        """
        Updates the settings UI elements to reflect the values stored in the database.

        :param data: List of setting tuples retrieved from the database.
        :type data: list
        """

        for key, value in data:
            if key == "theme":
                print(value)
                globals.settings_ui.cb_themes.setCurrentText(str(value))
