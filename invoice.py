from PyQt6 import QtCore, QtWidgets

from connection import Connection
import globals
from datetime import datetime
from reports import Reports


class InvoiceFormatter:
    """
        Utility class for formatting raw data into displayable strings for the Invoice UI.
    """

    @staticmethod
    def fullName(data):
        """
            Concatenates the surname and name from the data tuple.

            :param data: A list or tuple containing customer data.
                            Expected indices: [2] Name, [3] Surname.
            :return: A string representing the full name.
        """
        return f"{data[3]} {data[2]}"

    @staticmethod
    def fullAddress(data):
        """
            Formats the full address from the data tuple.

            :param data: A list or tuple containing customer data.
                             Expected indices: [6] Address, [7] City, [8] Zip Code.
            :return: A string representing the formatted address.
        """
        return f"{data[6]} {data[8]} {data[7]}"



class Invoice:
    """
        Manages the logic for the Invoice section of the application.
        Handles UI interactions, database CRUD operations for invoices and sales,
        and table management.
    """
    _dummy_customer = "00000000T"
    _all_data_boxes = []
    _mapping = {}

    @staticmethod
    def initDataBoxes():
        """
            Initializes the references to UI widgets and maps them to specific data indices.

            Sets up the `_mapping` dictionary used to populate customer details
            automatically when a search is performed.
        """
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
        """
            Searches for a customer by DNI and populates the invoice UI fields.

            Retrieves the DNI from the line edit. If the customer is not found,
            it defaults to the generic `_dummy_customer`. Populates labels
            based on the `_mapping` dictionary.
        """
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
        """
            Creates a new Invoice record in the database.

            Validates that a DNI exists. Generates the current date.
            If successful, updates the invoice table view. Displays
            success or error message boxes to the user.
        """

        try:
            dni = globals.ui.le_dni_invoice.text().upper().strip()

            today_date = datetime.now().strftime("%d/%m/%Y")

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
        """
            Clears all invoice-related UI fields and resets the sales table.

            Resets the row count to 1, unblocks signals, and re-enables editing triggers.
        """
        try:
            for box in Invoice._all_data_boxes:
                box.clear()

            globals.ui.table_sales.clearContents()
            globals.ui.table_sales.setRowCount(0)
            globals.ui.table_sales.setRowCount(1)
            globals.ui.table_sales.blockSignals(False)
            globals.ui.table_sales.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)

        except Exception as e:
            print(f"Error en clearData: {e}")

    @staticmethod
    def activeSales(create_new_row=False):
        """
            Configures the sales table structure and adds rows.

            :param create_new_row: If True, appends a new row to the end of the table.
                                   If False, resets the table to the initial state or current count.
        """
        try:
            sales_table = globals.ui.table_sales
            current_count = sales_table.rowCount()
            globals.ui.table_sales.blockSignals(True)
            if create_new_row:
                sales_table.setRowCount(current_count + 1)
                target_row = current_count
            else:
                if current_count == 0:
                    sales_table.setRowCount(1)
                    target_row = 0
                else:
                    target_row = current_count - 1

            item0 = QtWidgets.QTableWidgetItem("")
            item0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            sales_table.setItem(target_row, 0, item0)

            sales_table.setItem(target_row, 1, QtWidgets.QTableWidgetItem(""))
            sales_table.setItem(target_row, 2, QtWidgets.QTableWidgetItem(""))

            item3 = QtWidgets.QTableWidgetItem("")
            item3.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            sales_table.setItem(target_row, 3, item3)

            item4 = QtWidgets.QTableWidgetItem("")
            item4.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            sales_table.setItem(target_row, 4, item4)

            sales_table.blockSignals(False)

        except Exception as e:
            print(f"Error en activeSales: {e}")

    @staticmethod
    def cellChangedSales(item):
        """
            Event handler for changes in the sales table cells.

            Logic:
            - If Column 0 (Product ID) changes: Fetches product details and fills Name/Price.
            - If Column 3 (Quantity) changes: Calculates line total (Price * Quantity).
            - If the row is complete, calculates invoice totals and adds a new empty row.

            :param item: The QTableWidgetItem that was modified.
        """
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
                            mbox = QtWidgets.QMessageBox()
                            mbox.setWindowTitle("Warning")
                            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                            mbox.setText("There is no product with that ID")
                            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                            mbox.exec()
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
        """
            Calculates the Subtotal, IVA (VAT), and Total for the current invoice.

            Iterates through the sales table, sums the line totals, applies a 21% IVA,
            and updates the corresponding UI labels.
        """
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
    def setTableFacturaData(show_data_when_tab = False):
        """
            Retrieves all invoices from the database and populates the Invoice Table.

            :param show_data_when_tab: If True, automatically selects and displays data
                                        for the most recent invoice (index 0).
        """
        try:
            all_data_invoices = Connection.getAllInvoices()

            table = globals.ui.table_invoice
            index = 0
            for invoice in all_data_invoices:
                if show_data_when_tab and invoice == all_data_invoices[0]:
                    globals.ui.lbl_num_factura.setText(str(invoice[0]))
                    globals.ui.lbl_date_factura.setText(str(invoice[2]))

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
        """
            Handles the user selection of a specific invoice from the table.

            Populates header information (ID, Date, Customer).
            Locks the sales table for editing if the invoice already has saved sales.
            Loads the associated sales items.
        """
        try:
            row = globals.ui.table_invoice.selectedItems()
            data = [dato.text() for dato in row]

            globals.ui.lbl_num_factura.setText(data[0])
            globals.ui.le_dni_invoice.setText(data[1])
            globals.ui.lbl_date_factura.setText(data[2])
            Invoice.searchInvoiceCustomer()

            button_save_sale = globals.ui.btn_save_sale
            button_delete_invoice = globals.ui.btn_delete_invoice
            if not Connection.getSale(data[0]):
                globals.ui.table_sales.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)
                button_save_sale.setEnabled(True)
                button_delete_invoice.setEnabled(True)
            else:
                globals.ui.table_sales.blockSignals(True)
                globals.ui.table_sales.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
                button_delete_invoice.setEnabled(False)
                button_save_sale.setEnabled(False)

            Invoice.setTableSalesData(data[0])

        except Exception as e:
            print(f"Error en selectInvoice: {e}")

    @staticmethod
    def productRawDataToMap(data):
        """
            Converts raw database product tuples into a structured dictionary.

            :param data: Tuple containing product details.
            :return: Dictionary with keys: id, name, quantity, type, price, currency.
        """
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
        """
            Iterates through the sales table and saves each line item to the database.

            Validates that all required fields are present.
            If successful, prompts the user to print a ticket/report.
            Finally, clears the UI data.
        """
        try:
            table = globals.ui.table_sales
            id_factura = globals.ui.lbl_num_factura.text().strip()

            for r in range(table.rowCount()):
                id_product = table.item(r, 0).text().strip()
                product_name = table.item(r, 1).text().strip()
                unit_price = table.item(r, 2).text().strip()
                amount = table.item(r, 3).text().strip()
                total_item = table.item(r, 4).text().strip()

                if table.rowCount() == 1 and (not id_factura or not id_product or not product_name or not unit_price or not amount or not total_item):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Error")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setText("All data fields are required")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return

                # In case is an empty row
                if not product_name or not unit_price or not amount or not total_item:
                    continue

                if not Connection.addSale([id_factura, id_product, amount, product_name, unit_price, total_item]):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Error")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setText("Error saving the sales")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return


            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Success")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setText("Successfully saved the sales. Do you want to print the sale?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if mbox.exec():
                Reports.ticket()


            Invoice.clearData()

        except Exception as e:
            print(f"Error en saveSales: {e}")

    @staticmethod
    def setTableSalesData(id_factura):
        """
            Loads sales records associated with a specific invoice ID into the UI table.

            :param id_factura: The ID of the invoice to fetch sales for.
        """
        try:
            ui_table = globals.ui.table_sales

            ui_table.blockSignals(True)


            ui_table.clearContents()
            ui_table.setRowCount(0)

            all_sales = Connection.getSale(id_factura)

            if not all_sales:
                Invoice.activeSales(create_new_row=False)
                Invoice.calculateTotals()
                ui_table.blockSignals(False)
                return

            ui_table.setRowCount(len(all_sales))
            for index, sale in enumerate(all_sales):

                # ID Producto
                ui_table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(sale[2])))
                # Nombre Producto
                ui_table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(sale[3])))
                # Precio Unitario
                ui_table.setItem(index, 2, QtWidgets.QTableWidgetItem(str(sale[4])))
                # Cantidad
                ui_table.setItem(index, 3, QtWidgets.QTableWidgetItem(str(sale[5])))
                # Total Línea
                ui_table.setItem(index, 4, QtWidgets.QTableWidgetItem(str(sale[6])))

                item_align_center = QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
                item_align_left = QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter

                if ui_table.item(index, 0):
                    ui_table.item(index, 0).setTextAlignment(item_align_center)
                if ui_table.item(index, 1):
                    ui_table.item(index, 1).setTextAlignment(item_align_left)
                if ui_table.item(index, 2):
                    ui_table.item(index, 2).setTextAlignment(item_align_center)
                if ui_table.item(index, 3):
                    ui_table.item(index, 3).setTextAlignment(item_align_center)
                if ui_table.item(index, 4):
                    ui_table.item(index, 4).setTextAlignment(item_align_center)

            Invoice.calculateTotals()
            ui_table.blockSignals(False)
        except Exception as e:
            print("error en cargar setTableSalesData", e)

    @staticmethod
    def deleteInvoice():
        """
            Deletes the selected invoice and its associated sales from the database.

            Requires user confirmation via a message box.
            Refreshes the invoice list and clears fields upon success.
        """
        try:
            id_factura = globals.ui.lbl_num_factura.text().strip()

            mboxQuestion = QtWidgets.QMessageBox()
            mboxQuestion.setWindowTitle("Delete Invoice")
            mboxQuestion.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mboxQuestion.setText("Do you want to delete the invoice?")
            mboxQuestion.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mboxQuestion.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if mboxQuestion.exec() == QtWidgets.QMessageBox.StandardButton.No:
                mboxQuestion.hide()
                return

            if not id_factura:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setText("You need to select an invoice")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

            if not Connection.deleteInvoiceAndSale(id_factura):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Error deleting invoice")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Success")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setText("Successfully deleted the invoice")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()

            globals.ui.le_dni_invoice.setText("00000000T")
            Invoice.searchInvoiceCustomer()
            Invoice.activeSales()
        except Exception as e:
            print(f"Error en deleteInvoice: {e}")

    @property
    def dummy_customer(self):
        """
            Getter for the default dummy customer DNI.
        """
        return self._dummy_customer



