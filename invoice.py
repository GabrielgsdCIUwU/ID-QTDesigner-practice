from PyQt6 import QtCore, QtWidgets

from connection import Connection
import globals
from datetime import datetime


class InvoiceFormatter:
    @staticmethod
    def fullName(data):
        return f"{data[3]} {data[2]}"

    @staticmethod
    def fullAddress(data):
        return f"{data[6]} {data[8]} {data[7]}"



class Invoice:
    _dummy_customer = "00000000T"
    _all_data_boxes = []
    _mapping = {}

    @staticmethod
    def initDataBoxes():
        Invoice._all_data_boxes = [globals.ui.le_dni_invoice, globals.ui.lbl_date_factura , globals.ui.lbl_name_invoice , globals.ui.lbl_address_invoice, globals.ui.lbl_phone_invoice, globals.ui.lbl_invoicetype_invoice, globals.ui.lbl_status_invoice, globals.ui.lbl_num_factura]

        def display_historical(input_historical):
            if input_historical == "True":
                return "Active"

            return "Inactive"

        Invoice._mapping = {
            globals.ui.le_dni_invoice: lambda d: d[0],
            globals.ui.lbl_date_factura: lambda d: d[1],
            globals.ui.lbl_name_invoice: lambda d: InvoiceFormatter.fullName(d),
            globals.ui.lbl_address_invoice: lambda d: InvoiceFormatter.fullAddress(d),
            globals.ui.lbl_phone_invoice: lambda d: d[5],
            globals.ui.lbl_invoicetype_invoice: lambda d: d[9],
            globals.ui.lbl_status_invoice: lambda d: display_historical(d[10])
        }

    @staticmethod
    def searchInvoiceCustomer():
        try:
            dni = globals.ui.le_dni_invoice.text().upper().strip()
            customer_data = Connection.getCustomerData(dni, "dni")

            if not customer_data:
                customer_data = Connection.getCustomerData(Invoice._dummy_customer, "dni")

            globals.ui.le_dni_invoice.setText(dni)

            for box in Invoice._all_data_boxes:
                if box in Invoice._mapping:
                    box.setText(str(Invoice._mapping[box](customer_data)))


        except Exception as e:
            print(f"Error en saveInvoice: {e}")

    @staticmethod
    def saveInvoice():
        try:
            dni = globals.ui.le_dni_invoice.text().upper().strip()

            today_date = datetime.now().strftime("%d-%m-%Y")

            if not dni or not today_date:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setText("Missing Fields")
                mbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                mbox.exec()
                return

            data = [dni, today_date]

            if Connection.addInvoice(data):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Success saving the invoice")
                mbox.exec()
                Invoice.setTableFacturaData(True)
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText("An error has occurred while saving the invoice")
            mbox.exec()
            Invoice.setTableFacturaData(False)

        except Exception as e:
            print(f"Error en saveInvoice: {e}")

    @staticmethod
    def clearData():
        try:
            for box in Invoice._all_data_boxes:
                box.clear()


        except Exception as e:
            print(f"Error en clearData: {e}")

    @staticmethod
    def activeSales(create_new_row=False):
        try:
            sales_table = globals.ui.table_sales
            row_index = sales_table.rowCount()

            if create_new_row:
                sales_table.setRowCount(row_index + 1)
                row_index = row_index

            item0 = QtWidgets.QTableWidgetItem("")
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            sales_table.setItem(row_index, 0, item0)

            sales_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(""))
            sales_table.setItem(row_index, 2, QtWidgets.QTableWidgetItem(""))

            item3 = QtWidgets.QTableWidgetItem("")
            item3.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            sales_table.setItem(row_index, 3, item3)

            item4 = QtWidgets.QTableWidgetItem("")
            item4.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            sales_table.setItem(row_index, 4, item4)

        except Exception as e:
            print(f"Error en activeSales: {e}")

    @staticmethod
    def cellChangedSales(item):
        try:
            sales_table = globals.ui.table_sales
            current_row = item.row()
            current_col = item.column()

            if current_col not in (0, 3):
                return

            text_value = item.text().strip()
            if not text_value:
                return

            sales_table.blockSignals(True)
            try:
                if current_col == 0:
                    try:
                        product_row_data = Connection.getProductData(text_value, "id")
                        if not product_row_data:
                            return

                        product_map = Invoice.productRawDataToMap(product_row_data)

                        sales_table.setItem(current_row, 1, QtWidgets.QTableWidgetItem(str(product_map.get("name"))))
                        sales_table.setItem(current_row, 2, QtWidgets.QTableWidgetItem(str(product_map.get("price"))))
                        sales_table.item(current_row, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    except Exception as e:
                        print(f"Error al cargar producto: {e}")

                elif current_col == 3:
                    try:
                        price_item = sales_table.item(current_row, 2)
                        if price_item:
                            quantity = float(text_value)
                            price = float(price_item.text())
                            line_total = round(price * quantity, 2)

                            sales_table.setItem(current_row, 4, QtWidgets.QTableWidgetItem(str(line_total)))
                            sales_table.item(current_row, 4).setTextAlignment(
                                QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
                            )
                    except Exception as e:
                        print(f"Error al calcular total: {e}")
            finally:
                sales_table.blockSignals(False)

            row_complete = all([
                sales_table.item(current_row, 0) and sales_table.item(current_row, 0).text().strip(),
                sales_table.item(current_row, 1) and sales_table.item(current_row, 1).text().strip(),
                sales_table.item(current_row, 2) and sales_table.item(current_row, 2).text().strip(),
                sales_table.item(current_row, 3) and sales_table.item(current_row, 3).text().strip(),
                sales_table.item(current_row, 4) and sales_table.item(current_row, 4).text().strip()
            ])

            if row_complete:
                try:
                    Invoice.calculateTotals()
                    Invoice.activeSales(create_new_row=True)
                except Exception as e:
                    print(f"Error al añadir nueva fila o calcular totales: {e}")

        except Exception as e:
            print(f"Error en cellChangedSales: {e}")

    @staticmethod
    def calculateTotals():
        try:
            table = globals.ui.table_sales
            subtotal = 0.0
            iva = 0.21

            for r in range(table.rowCount()):
                total_item = table.item(r, 4)
                if total_item and total_item.text().strip():
                    try:
                        subtotal += float(total_item.text())
                    except:
                        pass

            total_iva = float(iva) * float(subtotal)
            total_to_pay = float(subtotal) + float(total_iva)

            globals.ui.lbl_subtotal_invoice.setText(str(round(subtotal, 2)))
            globals.ui.lbl_iva_invoice.setText(str(round(total_iva, 2)))
            globals.ui.lbl_total_invoice.setText(str(round(total_to_pay, 2)))

        except Exception as e:
            print(f"Error en calculateTotals: {e}")

    @staticmethod
    def setTableFacturaData(showData = False):
        try:
            all_data_invoices = Connection.getAllInvoices()

            table = globals.ui.table_invoice
            index = 0
            for invoice in all_data_invoices:
                if showData and invoice == all_data_invoices[0]:
                    globals.ui.lbl_num_factura.setText(invoice[0])
                    globals.ui.lbl_date_factura.setText(invoice[2])

                table.setRowCount(index + 1)
                table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(invoice[0])))
                table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(invoice[1])))
                table.setItem(index, 2, QtWidgets.QTableWidgetItem(str(invoice[2])))

                table.item(index, 0).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                table.item(index, 1).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                table.item(index, 2).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
                index += 1

            Invoice.searchInvoiceCustomer()
        except Exception as e:
            print(f"Error en setTableFacturaData: {e}")

    @staticmethod
    def selectInvoice():
        try:
            row = globals.ui.table_invoice.selectedItems()
            data = [dato.text() for dato in row]

            globals.ui.lbl_num_factura.setText(data[0])
            globals.ui.le_dni_invoice.setText(data[1])
            globals.ui.lbl_date_factura.setText(data[2])
            Invoice.searchInvoiceCustomer()

        except Exception as e:
            print(f"Error en selectInvoice: {e}")

    @staticmethod
    def productRawDataToMap(data):
        try:
            return {
                "id": data[0],
                "name": data[1],
                "quantity": data[2],
                "type": data[3],
                "price": data[4],
                "currency": data[5],
            }
        except Exception as e:
            print(f"Error en productRawDataToMap: {e}")



    @staticmethod
    def saveSales():
        try:
            table = globals.ui.table_sales
            id_factura = globals.ui.lbl_num_factura.text().strip()
            for r in range(table.rowCount()):
                id_product = table.item(r, 0).text().strip()
                product_name = table.item(r, 1).text().strip()
                unit_price = table.item(r, 2).text().strip()
                amount = table.item(r, 3).text().strip()
                total_item = table.item(r, 4).text().strip()

                if not Connection.addSale([id_factura, id_product, product_name, int(amount), float(unit_price), float(total_item)]):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Error")
                    mbox.setText("Error saving the sales")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return

            print("imprimiendo factura")

        except Exception as e:
            print(f"Error en saveSales: {e}")



