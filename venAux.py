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
        super(About, self).__init__()
        globals.about = Ui_dlgAbout()
        globals.about.setupUi(self)
        globals.about.btn_close_about.clicked.connect(lambda: globals.about.hide())
        self.setStyleSheet(styles.load_stylesheet())


class FileDialog(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialog, self).__init__()

class Settings(QtWidgets.QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        globals.settings_ui = Ui_settings()
        globals.settings_ui.setupUi(self)
        globals.settings_ui.btn_cancel_settings.clicked.connect(lambda: globals.settings.hide())
        globals.settings_ui.btn_save_settings.clicked.connect(lambda: Events.saveSettings())
        self.setStyleSheet(styles.load_stylesheet())

        self.loadAllStyles()

    @staticmethod
    def loadSettings():

        if not Connection.getSettings():
            data = [("theme", "Dark")]
            if not Connection.saveSettings(data):
                print("Error while saving the settings")

        return Connection.getSettings()


    @staticmethod
    def loadAllStyles():
        globals.settings_ui.cb_themes.clear()
        globals.settings_ui.cb_themes.addItems(styles.get_all_styles())

    @staticmethod
    def displayCurrentSettings(data):

        for key, value in data:
            if key == "theme":
                print(value)
                globals.settings_ui.cb_themes.setCurrentText(str(value))
