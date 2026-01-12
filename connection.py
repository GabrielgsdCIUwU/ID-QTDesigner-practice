import os
import sqlite3

import globals

from PyQt6 import QtSql, QtWidgets

class Connection:
    """
        Handles all database interactions for the SQLite backend, including CRUD operations
        for customers, products, invoices, and sales.
    """
    @staticmethod
    def db_connection():
        """
        Initializes the connection to the SQLite database.

        Checks if the database file exists and attempts to open it using QtSql.

        :return: True if the connection is successful and the database is valid, False otherwise.
        :rtype: bool
        """
        ruta_db = './data/bbdd.sqlite'

        if not os.path.isfile(ruta_db):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(ruta_db)

        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

        query = QtSql.QSqlQuery()
        query.exec("SELECT name FROM sqlite_master WHERE type='table';")

        if not query.next():  # Si no hay tablas
            QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

        #QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
        #                                  QtWidgets.QMessageBox.StandardButton.Ok)
        return True

    @staticmethod
    def getProvinces():
        """
        Retrieves all province names from the database.

        :return: A list of all province names.
        :rtype: list
        """
        all_provinces = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                all_provinces.append(query.value(1))

        return all_provinces

    @staticmethod
    def getCities(province):
        """
        Retrieves all city names belonging to a specific province.

        :param province: The name of the province to filter by.
        :type province: str
        :return: A list of city names.
        :rtype: list
        """
        all_cities = []
        query = QtSql.QSqlQuery()

        query.prepare("select * from municipios where idprov = ( select idprov from provincias where provincia = :province);")
        query.bindValue(":province", province)

        if query.exec():
            while query.next():
                all_cities.append(query.value(1))
        return all_cities

    @staticmethod
    def getCustomers(historical=True):
        """
        Retrieves customers from the database.

        :param historical: If True, returns only active customers. If False, returns all.
        :type historical: bool
        :return: A list of lists containing customer data rows.
        :rtype: list
        """
        if historical:
            historical_query = "SELECT * FROM customers where historical = 'True' order by surname;"
        else:
            historical_query = "SELECT * FROM customers order by surname;"

        all_customers = []
        query = QtSql.QSqlQuery()
        query.prepare(historical_query)
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                all_customers.append(row)
        return all_customers

    @staticmethod
    def getCustomerData(data, type_search):
        """
        Fetches detailed information for a single customer based on DNI or phone number.

        :param data: The search term (DNI string or Phone string).
        :type data: str
        :param type_search: The category of search ("dni" or "phone").
        :type type_search: str
        :return: A list containing all fields for the found customer.
        :rtype: list
        """
        try:
            all_customer_data = []
            query = QtSql.QSqlQuery()
            if type_search == "phone":
                query.prepare("SELECT * FROM customers WHERE mobile = :mobile;")
                query.bindValue(":mobile", str(data).strip())
            elif type_search == "dni":
                query.prepare("SELECT * FROM customers WHERE dni_nie = :dni;")
                query.bindValue(":dni", str(data).strip())
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        all_customer_data.append(query.value(i))

            return all_customer_data
        except Exception as error:
            print("Error getCustomerData: ", error)
    @staticmethod
    def deleteCustomer(dni):
        """
        Performs a logical deletion of a customer by setting their historical status to False.

        :param dni: The DNI/NIE of the customer to "delete".
        :type dni: str
        :return: True if the update was successful, False otherwise.
        :rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers set historical = :value WHERE dni_nie = :dni;")
            query.bindValue(":value", str(False))
            query.bindValue(":dni", dni)
            if not query.exec():
                return False
            return True
        except Exception as error:
            print("Error deleteCustomer: ", error)
        return True

    @staticmethod
    def addCustomer(data):
        """
        Inserts a new customer record into the database.

        :param data: A list containing UI elements or strings in the required order.
        :type data: list
        :return: True if insertion was successful, False otherwise.
        :rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO customers (dni_nie, adddata, surname, name, mail, mobile,"
                          "address, province, city, invoicetype, historical) VALUES (:dni_nie, :adddata, :surname, :name, :mail, :mobile,"
                          ":address, :province, :city, :invoicetype, :historical)")

            order_values = [":dni_nie", ":adddata", ":surname", ":name", ":mail", ":mobile",
                            ":address", ":province", ":city", ":invoicetype"]

            radial_buttons = ["electronic", "paper"]
            for i in range(len(order_values)):
                try:
                    if data[i] in radial_buttons:
                        value_text = data[i]
                    else:
                        value_text = str(data[i].text())
                except AttributeError:
                    value_text = str(data[i].currentText())
                query.bindValue(order_values[i], value_text)

            query.bindValue(":historical", str(True))

            if not query.exec():
                return False

            return True


        except Exception as error:
            print("Error addCustomer: ", error)
            return False

    @staticmethod
    def setCustomerData(data):
        """
        Updates an existing customer's information in the database.

        :param data: A list containing updated values for all customer fields.
        :type data: list
        :return: True if the update was successful, False otherwise.
        :rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers set"
                          " adddata = :adddata, surname = :surname, name = :name, mail = :mail, mobile = :mobile,"
                          "address = :address, province = :province, city = :city, invoicetype = :invoicetype,"
                          " historical = :historical"
                          " WHERE dni_nie = :dni_nie;")

            order_values = [":dni_nie", ":adddata", ":surname", ":name", ":mail", ":mobile",
                            ":address", ":province", ":city", ":invoicetype"]

            radial_buttons = ["electronic", "paper"]
            for i in range(len(order_values)):
                try:
                    if data[i] in radial_buttons:
                        value_text = data[i]
                    else:
                        value_text = str(data[i].text())
                except AttributeError:
                    value_text = str(data[i].currentText())
                query.bindValue(order_values[i], value_text)

            query.bindValue(":historical", str(data[10]))

            if not query.exec():
                return False

            return True

        except Exception as error:
            print("Error setCustomerData: ", error)

    @staticmethod
    def saveSettings(data):
        """
            Saves or replaces application settings in the database.

            :param data: A list of tuples containing (setting_id, value).
            :type data: list
            :return: True if all settings were saved successfully, False otherwise.
            :rtype: bool
        """
        try:
            for key, value in data:
                print(key, value)
                query = QtSql.QSqlQuery()
                query.prepare("INSERT OR REPLACE INTO settings (id, value) VALUES (:id, :value);")
                query.bindValue(":id", str(key))
                query.bindValue(":value", str(value))

                if not query.exec():
                    return False

            return True

        except Exception as error:
            print("Error saveSettings: ", error)

    @staticmethod
    def getSettings():
        """
            Retrieves all application configuration settings from the database.

            :return: A list of tuples containing (id, value).
            :rtype: list
        """
        try:
            all_settings = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM settings")
            if query.exec():
                while query.next():
                    all_settings.append((query.value(0), query.value(1)))

            return all_settings
        except Exception as error:
            print("Error getSettings: ", error)



    # products section
    @staticmethod
    def getProducts():
        """
        Retrieves all product records from the products table.

        :return: A list of lists containing product data.
        :rtype: list
        """
        historical_query = "SELECT * FROM products;"


        all_products = []
        query = QtSql.QSqlQuery()
        query.prepare(historical_query)
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                all_products.append(row)
        return all_products

    @staticmethod
    def addProduct(data):
        """
        Inserts a new product into the inventory database.

        :param data: A list containing [name, stock, family, price, currency].
        :type data: list
        :return: True if the product was added, False otherwise.
        :rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO products (name, stock, family, unit_price, currency) VALUES (:name, :stock, :family, :unit_price, :currency)")

            order_values = [":name", ":stock", ":family", ":unit_price", ":currency"]

            for i in range(len(order_values)):
                try:
                    value_text = str(data[i].text())
                except AttributeError:
                    value_text = str(data[i].currentText())
                query.bindValue(order_values[i], value_text)

            if not query.exec():
                return False

            return True

        except Exception as error:
            print("Error addProduct: ", error)

    @staticmethod
    def getProductData(product, search_type ="name"):
        """
        Retrieves specific product data by name or ID code.

        :param product: The identifier (Name string or Code integer).
        :type product: str|int
        :param search_type: The type of search ("name" or "id").
        :type search_type: str
        :return: A list containing the product record fields.
        :rtype: list
        """
        try:
            all_product_data = []
            query = QtSql.QSqlQuery()

            if search_type == "name":
                query.prepare("SELECT * FROM products WHERE name = :name")
                query.bindValue(":name", product)
            elif search_type == "id":
                query.prepare("SELECT * FROM products WHERE code = :id")
                query.bindValue(":id", product)

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        all_product_data.append((query.value(i)))

            return all_product_data
        except Exception as error:
            print("Error getProductData: ", error)

    @staticmethod
    def deleteProduct(product_name):
        """
        Permanently removes a product from the database by its name.

        :param product_name: The name of the product to delete.
        :type product_name: str
        :return: True if deletion was successful, False otherwise.
        :rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM products WHERE name = :name")
            query.bindValue(":name", str(product_name))

            if not query.exec():
                return False

            return True
        except Exception as error:
            print("Error deleteProduct: ", error)

    @staticmethod
    def setProductData(data):
        """
        Updates product information such as stock, family, or price.

        :param data: A list containing the updated product fields.
        :type data: list
        :return: True if the update was successful, False otherwise.
        :rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE products SET "
                      "name = :name, stock = :stock, family = :family, unit_price = :unit_price, currency = :currency "
                      "WHERE name = :name;")

            order_values = [":name", ":stock", ":family", ":unit_price", ":currency"]

            for i in range(len(order_values)):
                try:
                    value_text = str(data[i].text())
                except AttributeError:
                    value_text = str(data[i].currentText())
                query.bindValue(order_values[i], value_text)

            if not query.exec():
                return False

            return True
        except Exception as error:
            print("Error setCustomerData: ", error)


    # Invoice section
    @staticmethod
    def addInvoice(data):
        """
        Registers a new invoice associated with a customer.

        :param data: A list containing [dni, date_string].
        :type data: list
        :return: True if the invoice was created, False otherwise.
        :rtype: bool
        """
        # ! DATA FORMAT IS ["String", "String"...] NOT [globals.ui...]
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO invoices (dni_nie, date) VALUES (:dni, :date)")

            order_values = [":dni", ":date"]

            for i in range(len(order_values)):
                query.bindValue(order_values[i], str(data[i]))

            if not query.exec():
                return False

            return True

        except Exception as error:
            print("Error addInvoice: ", error)

    @staticmethod
    def getAllInvoices():
        """
        Retrieves all invoices sorted by ID in descending order.

        :return: A list of lists containing invoice records.
        :rtype: list
        """
        try:
            all_data_invoices = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices order by idFac desc;")

            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    all_data_invoices.append(row)

            return all_data_invoices

        except Exception as error:
            print("Error getAllInvoices: ", error)



    @staticmethod
    def addSale(data):
        """
        Adds an individual sale item linked to a specific invoice ID.

        :param data: List: [invoice_id, product_id, amount, name, unit_price, total].
        :type data: list
        :return: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO sales (idFactura, idProducto, amount, product, unitprice, total)"
                          "values (:idFactura, :idProduct, :amount, :product, :unitprice, :total)"
                          )

            order_values = [":idFactura", ":idProduct", ":amount", ":product", ":unitprice", ":total"]

            for i in range(len(order_values)):
                query.bindValue(order_values[i], str(data[i]))

            if not query.exec():
                return False

            return True

        except Exception as error:
            print("Error addSale: ", error)


    @staticmethod
    def getSale(id_factura):
        """
        Retrieves all line items (sales) associated with a specific invoice.

        :param id_factura: The ID of the parent invoice.
        :type id_factura: int|str
        :return: A list of sale records.
        :rtype: list
        """
        try:
            all_data_sales = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM sales where idFactura = :idFactura;")

            query.bindValue(":idFactura", int(id_factura))

            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    all_data_sales.append(row)

            print(all_data_sales)
            return all_data_sales

        except Exception as error:
            print("Error getSale: ", error)

    @staticmethod
    def deleteInvoice(id_factura):
        """
            Deletes an invoice header record.

            :param id_factura: The ID of the invoice to delete.
            :type id_factura: int|str
            :return: True if successful.
            :rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM invoices WHERE idFac = :idFac")
            query.bindValue(":idFac", str(id_factura))

            if not query.exec():
                return False

            return True
        except Exception as error:
            print("Error deleteInvoice: ", error)

    @staticmethod
    def deleteSale(id_factura):
        """
            Deletes all sale line items associated with a specific invoice.

            :param id_factura: The ID of the invoice whose sales should be removed.
            :type id_factura: int|str
            :return: True if successful.
            :rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM sales WHERE idFactura = :idFac")
            query.bindValue(":idFac", str(id_factura))

            if not query.exec():
                return False

            return True
        except Exception as error:
            print("Error deleteSale: ", error)

    @staticmethod
    def deleteInvoiceAndSale(id_factura):
        """
            Atomic operation to delete both the invoice and all its associated sales items.

            :param id_factura: The ID of the invoice to purge.
            :type id_factura: int|str
            :return: True if both operations succeeded, False otherwise.
            :rtype: bool
        """
        if not Connection.deleteSale(id_factura):
            return False

        if not Connection.deleteInvoice(id_factura):
            return False

        return True