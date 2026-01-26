import customers
from connection import *

from events import Events
import globals
from venAux import Calendar, About, FileDialog, Settings
from window import *
from customers import Customers
from products import Products
from invoice import Invoice
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
        self.connect_keyboard_signals()

        globals.theme_manager = ThemeManager()
        globals.theme_manager.register(self)
        globals.theme_manager.register(globals.settings)
        globals.theme_manager.register(globals.about)
        globals.theme_manager.register(globals.vencal)

        Invoice.initDataBoxes()

    def connect_signals_slot(self):
        #conexion DB
        Customers.setTableData()
        Products.setTableData()
        Invoice.setTableFacturaData()
        Events.resizeCustomerTable()
        Events.resizeProductTable()
        Events.resizeSalesTable()

        #File
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.dlg_about.triggered.connect(Events.messageAbout)
        globals.ui.actionSettings.triggered.connect(Events.settingsWindow)
        globals.ui.actionExportCustomers.triggered.connect(Events.exportCustomersToCsv)


        #Reports
        globals.ui.actionCustomerReport.triggered.connect(Reports.reportCustomers)
        globals.ui.actionProductReport.triggered.connect(Reports.reportProducts)
        globals.ui.actionTicketReport.triggered.connect(Reports.ticket)
        globals.ui.actionProductLowStockReport.triggered.connect(lambda: Reports.reportProducts(True))
        globals.ui.actionProductbyfamilyReport.triggered.connect(self.showFamilyReportSelector)

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

        #Fuctions Buttons in Invoice
        globals.ui.btn_save_invoice.clicked.connect(Invoice.saveInvoice)
        globals.ui.btn_clear_invoice.clicked.connect(Invoice.clearData)
        globals.ui.le_dni_invoice.editingFinished.connect(Invoice.searchInvoiceCustomer)
        globals.ui.btn_save_sale.clicked.connect(Invoice.saveSales)
        globals.ui.btn_delete_invoice.clicked.connect(Invoice.deleteInvoice)
        globals.ui.btn_delete_sale_row.clicked.connect(Invoice.deleteSaleRow)

        #Other functions in Invoice
        globals.ui.le_dni_invoice.setText("00000000T")
        Invoice.searchInvoiceCustomer()
        Invoice.activeSales()
        globals.ui.table_sales.itemChanged.connect(Invoice.cellChangedSales)

        #Function of tables
        globals.ui.table_customer.clicked.connect(Customers.selectCustomer)
        globals.ui.table_product.clicked.connect(Products.selectProduct)
        globals.ui.table_invoice.clicked.connect(Invoice.selectInvoice)

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


    def connect_keyboard_signals(self):
        #Invoice
        self.shortcutCleanInvoice = QtGui.QShortcut(QtGui.QKeySequence("F11"), self)
        self.shortcutCleanInvoice.activated.connect(Invoice.clearData)



    @staticmethod
    def setDefaultValues():
        globals.ui.le_date.setText('')

    def showFamilyReportSelector(self):
        try:
            families = Connection.getProductFamilies()

            if not families:
                QtWidgets.QMessageBox.warning(self,"Family Report", "No families selected")
                return

            family_selected, ok = QtWidgets.QInputDialog.getItem(
                self,
                "Select Family",
                "Select a family of products",
                families,
                0,
                False
            )

            if ok and family_selected:
                Reports.reportProducts(stock_family=family_selected)
        except Exception as error:
            print("Error showFamilyReportSelector: ", error)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
