import datetime

from PIL import Image
from reportlab.pdfgen import canvas
import os
import globals

from connection import Connection


class Reports:
    """
        Generates PDF reports and documents (Tickets, Customer Lists, Product Lists)
        using ReportLab.
    """
    REPORT_DIR = ".\\data\\reports\\"
    IMG_DIR = ".\\img\\"
    DUMMY_CUSTOMER = "00000000T"

    COLUMNS_CUSTOMERS = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE_TYPE", "STATE"]
    COORDS_CUSTOMERS = [(45, 650), (105, 650), (185, 650), (245, 650), (325, 650), (380, 650), (480, 650)]

    COLUMNS_PRODUCTS = ["CODE", "NAME", "STOCK", "FAMILY", "PRICE", "CURRENCY"]
    COORDS_PRODUCTS = [(45, 650), (95, 650), (240, 650), (300, 650), (400, 650), (455, 650)]

    COLUMNS_TICKET = ["CODE", "NAME", "PRICE", "AMOUNT", "TOTAL"]
    COORDS_TICKET = [(55, 650), (160, 650), (280, 650), (380, 650), (480, 650)]

    @staticmethod
    def ticket():
        """
        Generates and opens a PDF ticket for the currently selected invoice.
        """
        try:
            dni = globals.ui.le_dni_invoice.text().strip()
            id_factura = globals.ui.lbl_num_factura.text().strip()

            if not dni or not id_factura:
                return

            pdf_path, report_name = Reports._prepare_file_path("ticket")

            title, customer_data = Reports._get_ticket_context(dni)

            c = canvas.Canvas(pdf_path)

            Reports.topHeaderReport(c, title)

            if customer_data:
                Reports._displayTicketData(c, customer_data)

            Reports.displayColumnDataHeaders(c, Reports.COLUMNS_TICKET, Reports.COORDS_TICKET)

            last_y_position = Reports._displayTicketSalesData(c, title, Connection.getSale(id_factura))

            Reports._displayTotalsData(c, last_y_position)

            Reports.footer(c, title)

            c.save()

            Reports._open_pdf(pdf_path)

        except Exception as e:
            print(f"Error en ticket: {e}")

    @staticmethod
    def _get_ticket_context(dni):
        """
        Aplica la regla de negocio:
        - Si es DNI Genérico (00000000T) -> Factura Simplificada y SIN datos de cliente.
        - Si es otro DNI -> Factura normal y CON datos de cliente.
        """
        if dni == Reports.DUMMY_CUSTOMER:
            title = "FACTURA SIMPLIFICADA"
            customer_data = None
        else:
            title = "FACTURA"
            customer_data = Connection.getCustomerData(dni, "dni")

        return title, customer_data

    @staticmethod
    def _displayTicketData(c, data):
        """Pinta los datos del cliente en el ticket."""
        try:
            c.setFont("Helvetica-Bold", 10)

            c.drawString(250, 790, f"DNI: {str(data[0])}")
            c.drawString(250, 775, f"APELLIDOS: {str(data[2])}")
            c.drawString(250, 760, f"NOMBRE: {str(data[3])}")
            c.drawString(250, 745, f"DIRECCIÓN: {str(data[6])}")
            c.drawString(250, 730, f"LOCALIDAD: {str(data[8])} PROVINCIA: {str(data[7])}")
        except Exception as e:
            print(f"Error en _displayTicketData: {e}")


    @staticmethod
    def reportCustomers():
        """
            Generates a PDF containing the full list of customers.
        """
        print("Report Customers")
        try:
            title = "Customers"
            pdf_path, _ = Reports._prepare_file_path("customers")

            all_customers_data = Connection.getCustomers(False)

            c = canvas.Canvas(pdf_path)
            Reports.topHeaderReport(c, title)

            Reports.displayColumnDataHeaders(c, Reports.COLUMNS_CUSTOMERS, Reports.COORDS_CUSTOMERS)

            Reports.footer(c, title)
            Reports._displayCustomersData(c, all_customers_data)

            c.save()
            Reports._open_pdf(pdf_path)

        except Exception as e:
            print(f"Error en reportCustomers: {e}")

    @staticmethod
    def reportProducts():
        """
            Generates a PDF containing the full inventory list.
        """
        print("Report Products")
        try:
            title = "Products List"
            pdf_path, _ = Reports._prepare_file_path("products")

            all_products_data = Connection.getProducts()

            c = canvas.Canvas(pdf_path)
            Reports.topHeaderReport(c, title)
            Reports.displayColumnDataHeaders(c, Reports.COLUMNS_PRODUCTS, Reports.COORDS_PRODUCTS)
            Reports._displayProdutsData(c, all_products_data)
            Reports.footer(c, title)

            c.save()
            Reports._open_pdf(pdf_path)

        except Exception as e:
            print(f"Error en reportProducts: {e}")

    # ==========================================
    # HELPERS DE IO (Archivos y Rutas)
    # ==========================================

    @staticmethod
    def _prepare_file_path(suffix_name):
        """Crea el directorio si no existe y devuelve la ruta completa del PDF."""
        if not os.path.exists(Reports.REPORT_DIR):
            os.makedirs(Reports.REPORT_DIR)

        date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_name = f"{date_str}_{suffix_name}.pdf"
        full_path = os.path.join(Reports.REPORT_DIR, report_name)

        return full_path, report_name

    @staticmethod
    def _open_pdf(pdf_path):
        """Abre el archivo PDF generado usando el visor por defecto del sistema."""
        if os.path.exists(pdf_path):
            os.startfile(pdf_path)

    # ==========================================
    # HELPERS DE DIBUJO (Draw logic)
    # ==========================================

    @staticmethod
    def topHeaderReport(canvas_obj, title):
        """
            Draws the standard business header and logo on a PDF page.

            :param canvas_obj: ReportLab canvas.
            :param title: The report title.
            :type title: str
        """
        try:
            logo_path = os.path.join(Reports.IMG_DIR, "gabrielgsd.jpg")

            Reports.displayBusinessData(canvas_obj)

            # Cuadrado decorativo
            canvas_obj.line(20, 800, 120, 800)
            canvas_obj.line(20, 700, 120, 700)
            canvas_obj.line(20, 700, 20, 800)
            canvas_obj.line(120, 700, 120, 800)

            canvas_obj.setFont("Helvetica", 10)
            canvas_obj.drawCentredString(55, 785, "Empresa Teis")
            canvas_obj.drawCentredString(300, 675, title)
            canvas_obj.line(35, 665, 525, 665)

            try:
                logo = Image.open(logo_path)
                if isinstance(logo, Image.Image):
                    canvas_obj.drawImage(logo_path, 480, 745, width=40, height=40)
            except Exception as e:
                print(f"No se pudo cargar el logo: {e}")

        except Exception as e:
            print(f"Error en Reports top header: {e}")

    @staticmethod
    def displayBusinessData(canvas_obj):
        try:
            canvas_obj.setFont("Helvetica", 9)
            x = 25
            data = [
                "CIF: A12345678",
                "Avda. de Galicia, 101",
                "Vigo - 36215- España",
                "Tlfo: 986123456",
                "email: teis@mail.com"
            ]
            y = 755
            for line in data:
                canvas_obj.drawString(x, y, line)
                y -= 10
        except Exception as e:
            print(f"Error en displayBusinessData: {e}")

    @staticmethod
    def footer(canvas_obj, title):
        try:
            canvas_obj.line(35, 50, 525, 50)
            today = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
            canvas_obj.setFont("Helvetica", 7)
            canvas_obj.drawString(45, 40, today)
            canvas_obj.drawString(250, 40, title)
            canvas_obj.drawString(450, 40, f"Page: {canvas_obj.getPageNumber()}")
        except Exception as e:
            print(f"Error en footer: {e}")

    @staticmethod
    def displayColumnDataHeaders(canvas_obj, columns_list, coords_list):
        try:
            canvas_obj.setFont("Helvetica", 10)
            for i in range(len(columns_list)):
                x, y = coords_list[i]
                canvas_obj.drawString(x, y, str(columns_list[i]))
            canvas_obj.line(35, 645, 525, 645)
        except Exception as e:
            print(f"Error en headers: {e}")

    @staticmethod
    def displayMaxDataLengthFromData(data, length=15):
        if len(data) > length:
            return data[:length] + "..."
        return data

    @staticmethod
    def _displayHumanReadHistorical(historical):
        return "Active" if bool(historical) else "Inactive"

    @staticmethod
    def _createNextPage(canvas_obj, title, columns, coords):
        canvas_obj.setFont("Helvetica-Oblique", 8)
        canvas_obj.drawString(450, 75, "Página siguiente...")
        canvas_obj.showPage()

        Reports.displayColumnDataHeaders(canvas_obj, columns, coords)
        Reports.footer(canvas_obj, title)
        Reports.topHeaderReport(canvas_obj, title)
        canvas_obj.setFont("Helvetica", 10)


    @staticmethod
    def _displayCustomersData(c, all_customers_data):
        x = 55
        y = 630
        for customer in all_customers_data:
            if y <= 90:
                y = 630
                Reports._createNextPage(c, "Customers", Reports.COLUMNS_CUSTOMERS, Reports.COORDS_CUSTOMERS)

            c.setFont("Helvetica", 8)


            dni = "****" + str(customer[0][4:7] + "****")
            c.drawString(x - 7, y, dni)
            c.drawString(x + 50, y, Reports.displayMaxDataLengthFromData(str(customer[2])))
            c.drawString(x + 130, y, Reports.displayMaxDataLengthFromData(str(customer[3])))
            c.drawString(x + 190, y, Reports.displayMaxDataLengthFromData(str(customer[5])))
            c.drawString(x + 270, y, Reports.displayMaxDataLengthFromData(str(customer[8])))
            c.drawString(x + 350, y, Reports.displayMaxDataLengthFromData(str(customer[9])))
            c.drawString(x + 430, y, Reports._displayHumanReadHistorical(customer[10]))

            y -= 25


    @staticmethod
    def _displayProdutsData(c, all_products_data):
        y = 630
        for product in all_products_data:
            if y <= 90:
                y = 630
                Reports._createNextPage(c, "Products List", Reports.COLUMNS_PRODUCTS, Reports.COORDS_PRODUCTS)

            c.setFont("Helvetica", 8)
            c.drawString(45, y, str(product[0]))
            c.drawString(95, y, Reports.displayMaxDataLengthFromData(str(product[1]), length=25))
            c.drawString(245, y, str(product[2]))
            c.drawString(300, y, Reports.displayMaxDataLengthFromData(str(product[3])))

            try:
                price = "{:.2f}".format(product[4])
            except:
                price = str(product[4])
            c.drawString(400, y, price)
            c.drawString(480, y, str(product[5]))

            y -= 25

    @staticmethod
    def _displayTicketSalesData(c, title, all_tickets_data):

        y = 630
        for product in all_tickets_data:
            if y <= 90:
                y = 630
                Reports._createNextPage(c, title, Reports.COLUMNS_TICKET, Reports.COORDS_TICKET)

            c.setFont("Helvetica", 8)
            c.drawString(Reports.COORDS_TICKET[0][0], y, str(product[2]))
            c.drawString(Reports.COORDS_TICKET[1][0], y, Reports.displayMaxDataLengthFromData(str(product[4]), length=25))

            try:
                unit_price = "{:.2f}".format(product[5])
            except:
                unit_price = str(product[4])

            c.drawString(Reports.COORDS_TICKET[2][0], y, unit_price)
            c.drawString(Reports.COORDS_TICKET[3][0], y, str(product[3]))

            try:
                total_price = "{:.2f}".format(product[6])
            except:
                total_price = str(product[4])

            c.drawString(Reports.COORDS_TICKET[4][0], y, total_price)

            y -= 25

        return y

    @staticmethod
    def _displayTotalsData(c, y):
        try:
            if y < 150:
                c.showPage()
                y = 700

            x_label = 400
            x_value = 520

            c.setLineWidth(1)
            c.line(350, y, 525, y)
            y -= 20

            c.setFont("Helvetica-Bold", 8)

            subtotal = globals.ui.lbl_subtotal_invoice.text()
            iva = globals.ui.lbl_iva_invoice.text()
            total = globals.ui.lbl_total_invoice.text()

            c.drawString(x_label, y, "Subtotal:")
            c.drawRightString(x_value, y, f"{subtotal} €")

            y -= 15
            c.drawString(x_label, y, "IVA (21%):")
            c.drawRightString(x_value, y, f"{iva} €")

            y -= 20

            c.line(350, y +15, 525, y +15)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(x_label, y, "Total:")
            c.drawRightString(x_value, y, f"{total} €")
        except Exception as e:
            print(f"Error en _displayTotalsData: {e}")
