import re

from PyQt6 import QtCore, QtWidgets
from utils.utils import Utils

import globals
from connection import Connection
from events import Events
class Customers:
    @staticmethod
    def checkDni():
        try:
            globals.ui.le_dni.editingFinished.disconnect(Customers.checkDni)
            dni = globals.ui.le_dni.text()
            dni = str(dni).upper()
            globals.ui.le_dni.setText(dni)
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    globals.ui.le_dni.setStyleSheet('background-color: rgb(255, 255, 220); color: black')
                    return None

            globals.ui.le_dni.setStyleSheet('background-color:#FFC0CB; color black')
            globals.ui.le_dni.setText(None)
            #globals.ui.le_dni.setFocus()
        except Exception as error:
            print("error en validar dni ", error)
        finally:
            globals.ui.le_dni.editingFinished.connect(Customers.checkDni)

    @staticmethod
    def capitalizar(texto, widget):
        try:
            texto = texto.title()
            widget.setText(texto)
        except Exception as error:
            print("error en capitalizar texto ", error)

    @staticmethod
    def checkMail(email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(patron, email):
            globals.ui.le_email.setStyleSheet('background-color: rgb(255, 255, 220); color: black;')
        else:
            globals.ui.le_email.setStyleSheet('background-color: #FFC0CB; color: black;')
            globals.ui.le_email.setText(None)
            globals.ui.le_email.setPlaceholderText("Invalid Email")
            #globals.ui.le_email.setFocus()

    @staticmethod
    def checkMobil(numero):
        patron = r'^[67]\d{9}$'
        if re.match(patron, numero):
            globals.ui.le_email.setStyleSheet('background-color: rgb(255, 255, 220); color: black;')
        else:
            globals.ui.le_phone.setStyleSheet('background-color: #FFC0CB; color: black;')
            globals.ui.le_phone.setText(None)
            globals.ui.le_phone.setPlaceholderText("Invalid Mobile")
            #globals.ui.le_phone.setFocus()

    @staticmethod
    def setTableData(historical=True):
        try:
            all_customers = Connection.getCustomers(historical)

            def display_historical(input_historical):
                if input_historical == "True":
                    return "Active"

                return "Inactive"

            index = 0
            ui_table = globals.ui.table_customer
            for customer in all_customers:
                ui_table.setRowCount(index + 1)
                ui_table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(customer[2])))
                ui_table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(customer[3])))
                ui_table.setItem(index, 2, QtWidgets.QTableWidgetItem(str(customer[5])))
                ui_table.setItem(index, 3, QtWidgets.QTableWidgetItem(str(customer[7])))
                ui_table.setItem(index, 4, QtWidgets.QTableWidgetItem(str(customer[8])))
                ui_table.setItem(index, 5, QtWidgets.QTableWidgetItem(str(customer[9])))
                ui_table.setItem(index, 6, QtWidgets.QTableWidgetItem(display_historical(customer[10])))


                ui_table.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                ui_table.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                ui_table.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                ui_table.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                ui_table.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                ui_table.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                ui_table.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                index += 1

        except Exception as error:
            print("error en cargar setTableData ", error)

    @staticmethod
    def selectCustomer():
        try:
            #globals.ui.le_dni.setEnabled(False)
            Utils.clearStyles()
            Utils.disableLineEdit(globals.ui.le_dni)
            row_selected = globals.ui.table_customer.selectedItems()
            mobile_customer_selected = row_selected[2].text()
            all_customer_data = Connection.getCustomerData(str(mobile_customer_selected), "phone")

            all_data_boxes = [globals.ui.le_dni, globals.ui.le_date, globals.ui.le_surname, globals.ui.le_name,
                            globals.ui.le_email, globals.ui.le_phone, globals.ui.le_address]

            for i in range(len(all_data_boxes)):
                all_data_boxes[i].setText(str(all_customer_data[i]))

            globals.ui.cb_province.setCurrentText(str(all_customer_data[7]))
            globals.ui.cb_city.setCurrentText(str(all_customer_data[8]))

            if str(all_customer_data[9]) == "paper":
                globals.ui.rb_paper.setChecked(True)
            else:
                globals.ui.rb_electronic.setChecked(True)

            globals.status = all_customer_data[10]

            if globals.status == "True":
                globals.ui.lbl_status.setText("Active customer")
            else:
                globals.ui.lbl_status.setText("Inactive customer")

        except Exception as error:
            print("error en selectCustomer ", error)

    @staticmethod
    def deleteCustomer():
        try:
            Utils.disableLineEdit(globals.ui.le_dni)
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Customer?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if not mbox.exec():
                return

            dni = globals.ui.le_dni.text()
            print("dni: ", dni)

            if Connection.deleteCustomer(dni):
                mbox_success = QtWidgets.QMessageBox()
                mbox_success.setWindowTitle("Information")
                mbox_success.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox_success.setText("Success deleting the customer")
                mbox_success.exec()
                Customers.setTableData()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText("An error has occurred while deleting Customer")
            print("error en deleteCustomer ", dni)
        except Exception as error:
            print("error en deleteCustomer ", error)
    @staticmethod
    def getCustomersByHistorical():
        try:
            historical_checked = globals.ui.chkb_hystorical.isChecked()
            Customers.setTableData(historical_checked)
        except Exception as error:
            print("error en historicalCli ", error)

    @staticmethod
    def saveCustomer():
        try:
            all_data_boxes = [globals.ui.le_dni, globals.ui.le_date, globals.ui.le_surname, globals.ui.le_name,
                              globals.ui.le_email, globals.ui.le_phone, globals.ui.le_address, globals.ui.cb_province, globals.ui.cb_city]

            invoice_type = ""
            if globals.ui.rb_electronic.isChecked():
                invoice_type = "electronic"
            elif globals.ui.rb_paper.isChecked():
                invoice_type = "paper"

            all_data_boxes.append(invoice_type)

            if Connection.addCustomer(all_data_boxes):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Success saving the customer")
                mbox.exec()

                Utils.clearStyles()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText("An error has occurred while saving the customer")
            mbox.exec()
        except Exception as error:
            print("error en saveCustomer ", error)

    @staticmethod
    def clearData():
        try:
            all_data_boxes = [globals.ui.le_dni, globals.ui.le_date, globals.ui.le_surname, globals.ui.le_name,
                              globals.ui.le_email, globals.ui.le_phone, globals.ui.le_address]

            for i in range(len(all_data_boxes)):
                all_data_boxes[i].clear()

            Events.loadProvinces()
            Events.loadCities()
            globals.ui.rb_electronic.setChecked(True)
            globals.ui.le_dni.setEnabled(True)
            Utils.clearStyles()
        except Exception as e:
            print("Error clearData: ", e)

    @staticmethod
    def modifyCustomer():
        try:
            Utils.disableLineEdit(globals.ui.le_dni)
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Modify")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setText("Are you sure you want to modify the customer's data?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if not mbox.exec():
                mbox.hide()
                return

            all_data_boxes = [globals.ui.le_dni, globals.ui.le_date, globals.ui.le_surname, globals.ui.le_name,
                             globals.ui.le_email, globals.ui.le_phone, globals.ui.le_address, globals.ui.cb_province, globals.ui.cb_city]

            invoice_type = ""
            if globals.ui.rb_electronic.isChecked():
                invoice_type = "electronic"
            elif globals.ui.rb_paper.isChecked():
                invoice_type = "paper"

            all_data_boxes.append(invoice_type)

            if globals.status == "False":
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client inactive. Do you want to active the customer?")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

                if mbox.exec():
                    globals.status = "True"

            all_data_boxes.append(globals.status)

            if Connection.setCustomerData(all_data_boxes):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Success modifying the customer's data")
                mbox.exec()
                Utils.enableAllLineEdit()
                Customers.setTableData()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText("An error has occurred while modifying the customer's data")
            mbox.exec()

        except Exception as error:
            print("error en modifyCustomer ", error)

    @staticmethod
    def getCustomerById():
        try:
            #globals.ui.le_dni.setEnabled(False)
            Utils.disableLineEdit(globals.ui.le_dni)
            dni = globals.ui.le_dni.text()

            all_customer_data = Connection.getCustomerData(str(dni), "dni")
            if not all_customer_data:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Customer does not exist")
                mbox.exec()
                Utils.enableAllLineEdit()
                return

            all_data_boxes = [globals.ui.le_dni, globals.ui.le_date, globals.ui.le_surname, globals.ui.le_name,
                              globals.ui.le_email, globals.ui.le_phone, globals.ui.le_address]

            for i in range(len(all_data_boxes)):
                all_data_boxes[i].setText(str(all_customer_data[i]))

            globals.ui.cb_province.setCurrentText(str(all_customer_data[7]))
            globals.ui.cb_city.setCurrentText(str(all_customer_data[8]))

            if str(all_customer_data[9]) == "paper":
                globals.ui.rb_paper.setChecked(True)
            else:
                globals.ui.rb_electronic.setChecked(True)

            globals.status = all_customer_data[10]

            if globals.status == "True":
                globals.ui.lbl_status.setText("Active customer")
            else:
                globals.ui.lbl_status.setText("Inactive customer")


        except Exception as e:
            print("error en getCustomerById ", e)