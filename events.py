import csv
import datetime
import json
import os.path
import shutil
import sys
import time
import zipfile

from connection import *

from PyQt6 import  QtWidgets, QtCore, QtGui

import connection
import  globals
import customers
import styles


class Events:
    """
        Global event handlers for the application, including file operations,
        UI resizing, and system dialogs.
    """
    @staticmethod
    def messageExit(self=None):
        """
            Displays a confirmation dialog before closing the application.
        """
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setWindowIcon(QtGui.QIcon("img/gabrielgsd.jpg"))
            mbox.setWindowTitle('Exit')
            mbox.setText('Are you sure you want to exit?')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
            mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')

            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                sys.exit()
            else:
                mbox.hide()
        except Exception as e:
            print("Error en messageExit: ", e)

    @staticmethod
    def openCalendar(self=None):
        """
            Opens the modal calendar dialog.
        """
        try:
            globals.vencal.show()
        except Exception as e:
            print("Error en calendario: ", e)

    @staticmethod
    def loadData(qDate):
        """
            Transfers the selected date from the calendar to the main form.

            :param qDate: Selected date.
            :type qDate: QDate
        """
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if globals.ui.pan_main.currentIndex() == 0:
                globals.ui.le_date.setText(data)
            time.sleep(0.3)
            globals.vencal.hide()

        except Exception as e:
            print("error en cargar Data", e)

    @staticmethod
    def loadProvinces():
        """
            Loads the list of provinces into the corresponding combo box.
        """
        try:
            globals.ui.cb_province.clear()
            globals.ui.cb_province.addItems(Connection.getProvinces())
        except Exception as e:
            print("Error loading provinces: ", e)

    @staticmethod
    def loadCities():
        """
            Updates the city combo box based on the currently selected province.
        """
        try:
            globals.ui.cb_city.clear()
            province = globals.ui.cb_province.currentText()
            globals.ui.cb_city.addItems(Connection.getCities(province))
        except Exception as e:
            print("Error loading cities: ", e)

    @staticmethod
    def loadProductFamily():
        """
            Populates the product family combo box with predefined values.
        """
        try:
            globals.ui.cb_family.clear()
            all_product_family = ["Foods", "Furniture", "Clothes", "Electronic"]
            globals.ui.cb_family.addItems(all_product_family)
        except Exception as e:
            print("Error loading product family: ", e)

    @staticmethod
    def loadCurrency():
        """
            Populates the currency combo box with predefined symbols.
        """

        try:
            globals.ui.cb_currency.clear()
            all_currency = ["€", "$"]
            globals.ui.cb_currency.addItems(all_currency)
        except Exception as e:
            print("Error loading currency: ", e)


    @staticmethod
    def loadSettings():
        """
            Loads configuration settings (like themes) into the settings dialog.
        """
        try:
            globals.settings.cb_themes.clear()
            globals.settings.cb_themes.addItems(styles.get_all_styles())
        except Exception as e:
            print("Error loading settings: ", e)

    @staticmethod
    def resizeCustomerTable():
        """
            Configures header behavior and resizing for the Customer table.
        """
        try:
            header = globals.ui.table_customer.horizontalHeader()
            for i in range(header.count()):
                if i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.table_customer.horizontalHeaderItem(i)
                # negrita cabecera
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("Error resize customer table: ", e)

    @staticmethod
    def resizeProductTable():
        """
            Configures header behavior and resizing for the Product table.
        """
        try:
            header = globals.ui.table_product.horizontalHeader()
            for i in range(header.count()):
                if i in (0, 4):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.table_product.horizontalHeaderItem(i)
                # negrita cabecera
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("Error resize product table: ", e)

    @staticmethod
    def resizeSalesTable():
        """
            Configures header behavior and resizing for the Sales table.
        """
        try:
            header = globals.ui.table_sales.horizontalHeader()
            for i in range(header.count()):
                if i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.table_sales.horizontalHeaderItem(i)
                # negrita cabecera
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

            globals.ui.table_sales.setRowCount(1)
        except Exception as e:
            print("Error resize product table: ", e)

    @staticmethod
    def messageAbout():
        """
            Displays the "About" information dialog.
        """
        try:
            globals.about.show()
        except Exception as e:
            print("Error en messageAbout: ", e)

    @staticmethod
    def settingsWindow():
        """
            Initializes and displays the settings configuration window.
        """
        try:
            settings_data = globals.settings.loadSettings()
            globals.settings.displayCurrentSettings(settings_data)
            globals.settings.show()
        except Exception as e:
            print("Error en settingsWindow: ", e)

    @staticmethod
    def saveBackup():
        """
            Creates a compressed .zip backup of the SQLite database.
        """

        try:
            date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = str(date + '_backup.zip')
            file_path, _ = globals.dialog_open.getSaveFileName(None, "Save Backup file", filename, 'zip')

            if globals.dialog_open.accept and file_path:
                with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as filezip:
                    filezip.write('./data/bbdd.sqlite', os.path.basename('bbdd.sqlite'))

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("img/gabrielgsd.jpg"))
                mbox.setWindowTitle('Save Backup')
                mbox.setText('Done saving backup')
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText("An error has ocurred while saving the backup")
            mbox.setWindowTitle('Error')
            mbox.exec()

        except Exception as e:
            print("Error en saveBackup: ", e)
    @staticmethod
    def restoreBackup():
        """
            Restores a database file from a selected .zip backup.
        """
        try:
            filename = globals.dialog_open.getOpenFileName(None, "Restore Backup file", '', '*.zip;;All Files (*)')
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, 'r', zipfile.ZIP_DEFLATED) as bbdd:
                    bbdd.extractall(path='./data')

                bbdd.close()

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("img/gabrielgsd.jpg"))
                mbox.setWindowTitle('Successfully')
                mbox.setText('Successfully restored backup')
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

                connection.Connection.db_connection()
                Events.loadProvinces()
                Events.loadCities()
                customers.Customers.setTableData()
                from products import Products
                from invoice import Invoice
                Products.setTableData()
                Invoice.setTableFacturaData()

        except Exception as e:
            print("Error en restoreBackup: ", e)

    @staticmethod
    def importCustomersFromCsv():
        try:
            filename, _ = globals.dialog_open.getOpenFileName(
                None, "Import customer CSV", '', 'CSV Files (*.csv)'
            )
            if not filename: return

            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            new_count = 0
            update_count = 0
            final_data_to_import = []

            csv_header_order = [
                "DNI_NIE", "AddData", "Surname", "Name", "eMail", "Mobile",
                "Address", "Province", "City", "InvoiceType", "Active"
            ]

            for row in rows:
                dni = row.get("DNI_NIE", '').strip().upper()
                if not dni: continue

                if Connection.getCustomerData(dni, "dni"):
                    update_count += 1
                else:
                    new_count += 1

                formatted_row = [row.get(field, '') for field in csv_header_order]
                final_data_to_import.append(formatted_row)

            msg = (f"Summary of file: {len(rows)} records found.\n\n"
                   f"- New customers to be created: {new_count}\n"
                   f"- Existing customers to be updated: {update_count}\n\n"
                   f"Do you want to proceed with the import?"
                   )

            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setWindowIcon(QtGui.QIcon("img/gabrielgsd.jpg"))
            mbox.setWindowTitle('Confirm Import')
            mbox.setText(msg)
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.No:
                return

            if not Connection.importCustomers(final_data_to_import):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle("Database Error")
                mbox.setText("An error occurred while saving data to the database.")
                mbox.exec()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setWindowTitle("Success")
            mbox.setText("Data imported successfully.")
            mbox.exec()

            customers.Customers.setTableData()
            Events.loadProvinces()
            Events.loadCities()

        except Exception as e:
            print("Error en importCustomersFromCsv: ", e)

    @staticmethod
    def importProductsFromJson():
        try:
            filename, _ = globals.dialog_open.getOpenFileName(
                None, "Import Products JSON", '', 'JSON Files (*.json)'
            )
            if not filename: return

            with open(filename, mode='r', encoding='utf-8') as file:
                raw_data = json.load(file)

            new_count = 0
            update_count = 0
            final_data_to_import = []

            for product in raw_data:
                product_id = product.get('id')
                if not product_id: continue

                if Connection.getProductData(product_id, "id"):
                    update_count += 1
                else:
                    new_count += 1

                formatted_row = [
                    product.get('id'),
                    product.get('name'),
                    product.get('stock'),
                    #ni
                    product.get('family'),
                    product.get('price'),
                    product.get('currency', '€'),
                ]
                final_data_to_import.append(formatted_row)

            msg = (f"Summary of file: {len(raw_data)} records found.\n\n"
                   f"- New customers to be created: {new_count}\n"
                   f"- Existing customers to be updated: {update_count}\n\n"
                   f"Do you want to proceed with the import?"
                   )

            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setWindowIcon(QtGui.QIcon("img/gabrielgsd.jpg"))
            mbox.setWindowTitle('Confirm Import')
            mbox.setText(msg)
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.No:
                return

            if not Connection.importProducts(final_data_to_import):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle("Database Error")
                mbox.setText("An error occurred while saving data to the database.")
                mbox.exec()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setWindowTitle("Success")
            mbox.setText("Data imported successfully.")
            mbox.exec()

            from products import Products
            Products.clearData()
            Products.setTableData()

        except Exception as e:
            print("Error en importProductsFromJson: ", e)

    @staticmethod
    def exportCustomersToCsv():
        """
            Exports all customer data from the database to a CSV file.
        """
        try:
            date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = str(date + '_customers.csv')
            file_path, _ = globals.dialog_open.getSaveFileName(None, "Export customers data", filename, 'CSV Files (*.csv)')

            if file_path:
                all_customers_data = Connection.getCustomers(historical=False)
                with open(file_path, 'w', newline='', encoding='utf-8') as csvFile:
                    writer = csv.writer(csvFile)

                    header_rows = [
                        "dni_nie",
                        "adddata",
                        "surname",
                        "name",
                        "mail",
                        "mobile",
                        "address",
                        "province",
                        "city",
                        "invoicetype",
                        "historical"
                    ]

                    writer.writerow(header_rows)
                    writer.writerows(all_customers_data)



                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("img/gabrielgsd.jpg"))
                mbox.setWindowTitle('Exported customers')
                mbox.setText('Successfully exported customers data')
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setWindowTitle('Error')
            mbox.setText("An error has ocurred while exporting the customers data")
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()


        except Exception as e:
            print("Error en exportCustomersToXsl: ", e)
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setWindowTitle('Exception')
            mbox.setText("An unexpected error has occurred")
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()

    @staticmethod
    def saveSettings():
        """
            Saves user preferences (like theme) from the settings UI to the database.
        """
        try:
            all_settings_data = []

            # Themes
            new_theme = globals.settings_ui.cb_themes.currentText()
            all_settings_data.append(("theme", new_theme))

            if not Connection.saveSettings(all_settings_data):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Error')
                mbox.setText("An error has ocurred while saving the settings")
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setWindowIcon(QtGui.QIcon("img/gabrielgsd.jpg"))
            mbox.setWindowTitle('Successfully')
            mbox.setText('Successfully saved settings')
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()
            globals.settings.hide()
            globals.theme_manager.change_theme(new_theme)



        except Exception as e:
            print("Error en saveSettings: ", e)

    @staticmethod
    def showStatusBar():
        """
            Initializes the status bar with the current date and version number.
        """
        try:
            today = datetime.datetime.now().strftime("%d/%m/%Y")
            label_status = QtWidgets.QLabel()
            label_status.setText("Date: " + today + " - " + "Versión 0.0.1")
            label_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            globals.ui.statusbar.addPermanentWidget(label_status, 1)
        except Exception as e:
            print("Error en showStatusBar: ", e)
