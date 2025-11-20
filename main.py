import customers
from connection import *

from events import Events
import globals
from venAux import Calendar, About, FileDialog, Settings
from window import *
from customers import Customers
from products import Products
import styles
import  sys
from ThemeManager import ThemeManager
from reports import *

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_window()
        globals.ui.setupUi(self)

        # Iniciar DB antes de istanciar
        Connection.db_connection()

        #instance
        globals.vencal = Calendar()
        globals.about = About()
        globals.dialog_open = FileDialog()
        globals.settings = Settings()
        globals.theme = ThemeManager()


        self.connect_signals_slot()

        globals.theme_manager = ThemeManager()
        globals.theme_manager.register(self)
        globals.theme_manager.register(globals.settings)
        globals.theme_manager.register(globals.about)
        globals.theme_manager.register(globals.vencal)

    @staticmethod
    def connect_signals_slot():
        #conexion DB
        Customers.setTableData()
        Products.setTableData()
        Events.resizeCustomerTable()
        Events.resizeProductTable()

        #File
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.dlg_about.triggered.connect(Events.messageAbout)
        globals.ui.actionSettings.triggered.connect(Events.settingsWindow)
        globals.ui.actionExportCustomers.triggered.connect(Events.exportCustomersToCsv)
        globals.ui.actionCustomerReport.triggered.connect(Reports.reportCustomers)

        #Tools
        globals.ui.actionBackup.triggered.connect(Events.saveBackup)
        globals.ui.actionRestoreBackup.triggered.connect(Events.restoreBackup)

        #Customers
        globals.ui.le_dni.editingFinished.connect(Customers.checkDni)
        globals.ui.le_surname.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.le_surname.text(), globals.ui.le_surname))
        globals.ui.le_name.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.le_name.text(), globals.ui.le_name))
        globals.ui.le_email.editingFinished.connect(lambda: Customers.checkMail(globals.ui.le_email.text()))
        globals.ui.le_phone.editingFinished.connect(lambda: Customers.checkMobil(globals.ui.le_phone.text()))

        #Products
        globals.ui.le_name_product.editingFinished.connect(
            lambda: Customers.capitalizar(globals.ui.le_name_product.text(), globals.ui.le_name_product))
        globals.ui.le_unit_price.editingFinished.connect(Products.checkUnitPrice)


        #Functions Buttons
        globals.ui.btn_calendar.clicked.connect(Events.openCalendar)
        globals.ui.btn_del_cust.clicked.connect(Customers.deleteCustomer)
        globals.ui.btn_save_cust.clicked.connect(Customers.saveCustomer)
        globals.ui.btn_clear.clicked.connect(Customers.clearData)
        globals.ui.btn_modify_cust.clicked.connect(Customers.modifyCustomer)
        globals.ui.btn_search.clicked.connect(Customers.getCustomerById)

        #Functions Buttons in Sales
        globals.ui.btn_save_product.clicked.connect(Products.saveProduct)
        globals.ui.btn_clear_product.clicked.connect(Products.clearData)
        globals.ui.btn_delete_product.clicked.connect(Products.deleteProduct)
        globals.ui.btn_modify_product.clicked.connect(Products.modifyProduct)

        #Function of tables
        globals.ui.table_customer.clicked.connect(Customers.selectCustomer)
        globals.ui.table_product.clicked.connect(Products.selectProduct)

        # Function combobox
        Events.loadProvinces()
        globals.ui.cb_province.currentIndexChanged.connect(Events.loadCities)
        Events.loadProductFamily()
        Events.loadCurrency()

        # Functions of check Historical
        globals.ui.chkb_hystorical.setChecked(True)
        globals.ui.chkb_hystorical.stateChanged.connect(Customers.getCustomersByHistorical)

        #Show status bar
        Events.showStatusBar()



        # How to load a combo box from array
        # options = ["4%", "12%", "21%"]
        # globals.ui.cb_iva.addItems(options)


    @staticmethod
    def setDefaultValues():
        globals.ui.le_date.setText('')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
