import os
import sqlite3

import globals

from PyQt6 import QtSql, QtWidgets

class Connection:
    @staticmethod
    def db_connection():
        """
        Devuelve si la conexión con la base de datos tuvo éxito o no
        :return:
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
        Carga todas las provincias de la base de datos en SQL.
        :return: Lista de provincias
        :rtype: bytearray
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
        Pasando una provincia devuelve todas las ciudades de esa provincia.
        :param province: string
        :type province: basestring
        :return: Lista de ciudades
        :rtype: bytearray
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
        Devuelve todos los clientes con la base de datos en SQL.
        :param historical: true clientes activos. false todos los clientes
        :type historical: bool
        :return: Lista de clientes
        :rtype: bytearray
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
        Obten toda la información de un cliente con la base de datos en SQL.
        :param data: Móvil o DNI.
        :type data: basestring
        :param type_search: Tipo de dato a buscar: dni, phone.
        :type type_search: basestring
        :return: Lista con los datos del cliente.
        :rtype: bytearray
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
        Establecer el cliente como histórico.
        :param dni: DNI del cliente
        :type dni: basestring
        :return: Se ha ejecutado con éxito
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
        Dar de alta un cliente
        :param data: Datos del cliente
        :type data: bytearray
        :return: Se ha ejecutado con éxito
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
        Modifica los datos de un cliente
        :param data: Todos los nuevos datos del cliente. orden: [DNI, adddata, surname, name, mail, mobile, address, province, city, invoicetype]
        :type data: bytearray
        :return: Se ha ejecutado con éxito
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
        Obtener todos los productos de la base de datos
        :return: Lista con los productos
        :rtype: bytearray
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
        Añade un nuevo producto
        :param data: Datos del producto. Orden: [name, stock, family, unit_price, currency]
        :type data: bytearray
        :return: Se ha ejecutado con éxito
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
        Obtener toda la información de un producto
        :param product: Nombre del producto o ID
        :type product: basestring
        :param search_type: Tipo de búsqueda: name o id
        :type search_type: basestring
        :return: Lista con todos los datos del producto
        :rtype: bytearray
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
        Eliminar producto de la base de datos.
        :param product_name: Nombre del producto
        :type product_name: basestring
        :return: Se ha ejecutado con éxito
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
        Modificar datos de un producto en la base de datos
        :param data: Nuevos datos del producto. Orden: [name, stock, family, unit_price, currency]
        :type data: bytearray
        :return: Se ha ejecutado con éxito
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
        Añadir invoice a la base de datos
        :param data: Nuevo invoice. Orden: [dni, date]
        :type data: bytearray
        :return: Se ha ejecutado con éxito
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
        Obtener todos los invoices de la base de datos.
        :return: Lista con todos los invoices ordenador de forma descendente por idFac de la base de datos
        :rtype: bytearray
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
        Adding sale to the database
        :param data: Values order: idFactura, idProduct, Amount, Product, UnitPrice, Total
        :return: bool
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
        Obtener los datos de sale de la base de datos.
        :param id_factura: ID de la factura.
        :type id_factura: basestring
        :return: Todos los datos de sale.
        :rtype: bytearray
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
        if not Connection.deleteSale(id_factura):
            return False

        if not Connection.deleteInvoice(id_factura):
            return False

        return True