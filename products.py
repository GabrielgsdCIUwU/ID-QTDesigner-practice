
from connection import Connection
from PyQt6 import QtCore, QtWidgets
import globals
from events import Events
from utils.utils import Utils


class Products:

    @staticmethod
    def checkUnitPrice():
        price = globals.ui.le_unit_price.text()
        try:
            price_float = float(price)
            price = "{:.2f}".format(price_float)

            if price_float <= 0:
                globals.ui.le_unit_price.setStyleSheet('background-color:#FFC0CB; color black')
                globals.ui.le_unit_price.setText("")
                return

            globals.ui.le_unit_price.setStyleSheet('background-color: rgb(255, 255, 220); color: black')
            globals.ui.le_unit_price.setText(price)
        except ValueError:
            globals.ui.le_unit_price.setStyleSheet('background-color:#FFC0CB; color black')
            globals.ui.le_unit_price.setText("")

    @staticmethod
    def setTableData():
        try:
            all_products = Connection.getProducts()

            index = 0
            ui_table = globals.ui.table_product
            for product in all_products:
                ui_table.setRowCount(index + 1)
                ui_table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(product[1])))
                ui_table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(product[2])))
                ui_table.setItem(index, 2, QtWidgets.QTableWidgetItem(str(product[3])))
                ui_table.setItem(index, 3, QtWidgets.QTableWidgetItem(str(product[4])))
                ui_table.setItem(index, 4, QtWidgets.QTableWidgetItem(str(product[5])))

                ui_table.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                ui_table.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                ui_table.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                ui_table.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                ui_table.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                index += 1

        except Exception as e:
            print("error en cargar setTableData", e)

    @staticmethod
    def saveProduct():
        try:
            all_data_boxes = [globals.ui.le_name_product, globals.ui.le_stock, globals.ui.cb_family, globals.ui.le_unit_price, globals.ui.cb_currency]

            if Connection.addProduct(all_data_boxes):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Success saving the product")
                mbox.exec()
                Products.setTableData()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText("An error has occurred while saving the product")
            mbox.exec()

            Products.setTableData()

        except Exception as e:
            print("error en cargar saveProduct", e)

    @staticmethod
    def selectProduct():
        try:
            Utils.clearStyles()
            Utils.disableLineEdit(globals.ui.le_name_product)
            row_selected = globals.ui.table_product.selectedItems()
            name_product_selected = row_selected[0].text()
            all_product_data = Connection.getProductData(str(name_product_selected))

            all_data_boxes = [globals.ui.le_name_product, globals.ui.le_stock, globals.ui.cb_family, globals.ui.le_unit_price, globals.ui.cb_currency]

            for i in range(len(all_data_boxes)):
                if i == 2 or i == 4:
                    all_data_boxes[i].setCurrentText(str(all_product_data[i+1]))
                else:
                    all_data_boxes[i].setText(str(all_product_data[i+1]))

        except Exception as e:
            print("error en selectProduct", e)

    @staticmethod
    def clearData():
        try:
            all_data_boxes = [globals.ui.le_name_product, globals.ui.le_stock, globals.ui.le_unit_price, globals.ui.cb_currency]

            for i in range(len(all_data_boxes)):
                all_data_boxes[i].clear()

            Events.loadProductFamily()
            Events.loadCurrency()
            Utils.clearStyles()
            Utils.enableAllLineEdit()
        except Exception as e:
            print("error en clearData", e)

    @staticmethod
    def deleteProduct():
        try:
            Utils.disableLineEdit(globals.ui.le_name_product)
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Product?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if not mbox.exec():
                return

            name_product = globals.ui.le_name_product.text()

            if Connection.deleteProduct(name_product):
                mbox_success = QtWidgets.QMessageBox()
                mbox_success.setWindowTitle("Information")
                mbox_success.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox_success.setText("Success deleting the product")
                mbox_success.exec()
                Products.setTableData()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText("An error has occurred while deleting Product")
            print("error en deleteCustomer ", name_product)

        except Exception as e:
            print("error en deleteProduct", e)

    @staticmethod
    def modifyProduct():
        try:
            Utils.disableLineEdit(globals.ui.le_name_product)
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Modify")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setText("Are you sure you want to modify the product's data?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if not mbox.exec():
                mbox.hide()
                return

            all_data_boxes = [globals.ui.le_name_product, globals.ui.le_stock, globals.ui.cb_family,
                              globals.ui.le_unit_price, globals.ui.cb_currency]

            if Connection.setProductData(all_data_boxes):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Success modifying the product's data")
                mbox.exec()
                Utils.enableAllLineEdit()
                Products.setTableData()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText("An error has occurred while modifying the product's data")
            mbox.exec()

        except Exception as e:
            print("error en modifyProduct", e)
