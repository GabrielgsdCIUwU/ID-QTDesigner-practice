import datetime

from PIL import Image
from reportlab.pdfgen import canvas
import os

from connection import Connection




class Reports:
    columns_data = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE_TYPE", "STATE"]
    coords_columns = [(45, 650), (105, 650), (185, 650), (245, 650), (325, 650), (380, 650), (480, 650)]

    @staticmethod
    def reportCustomers():
        print("Report Customers")
        try:
            titleForCanvas = "Customers"
            date = "" #datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            root_path = ".\\data\\reports\\"
            report_name = f"{date}_customers.pdf"

            all_customers_data = Connection.getCustomers(False)

            pdf_path = os.path.join(root_path, report_name)
            customer_canvas = canvas.Canvas(pdf_path)

            Reports.topHeaderReport(customer_canvas, titleForCanvas)

            Reports.displayColumnDataHeaders(customer_canvas)

            Reports.footer(customer_canvas, titleForCanvas)

            Reports._displayCustomersData(customer_canvas, all_customers_data)

            customer_canvas.save()

            for file in os.listdir(root_path):
                if file.endswith(report_name):
                    os.startfile(pdf_path)
        except Exception as e:
            print(f"Error en reportCustomers: {e}" )

    @staticmethod
    def _displayCustomersData(customer_canvas, all_customers_data):
        x = 55
        y = 630
        for customer in all_customers_data:
            if y <= 90:
                y = 630
                #Construir la siguiente pagina
                title = "Customers"

                customer_canvas.setFont("Helvetica-Oblique", 8)
                customer_canvas.drawString(450, 75, "Página siguiente...")
                customer_canvas.showPage()

                Reports.displayColumnDataHeaders(customer_canvas)

                Reports.footer(customer_canvas, title)
                Reports.topHeaderReport(customer_canvas, title)

                customer_canvas.setFont("Helvetica", 10)



            customer_canvas.setFont("Helvetica", 8)

            # Data from customers to display
            dni = "****" + str(customer[0][4:7] + "****")
            customer_canvas.drawString(x - 7, y, dni)
            customer_canvas.drawString(x + 50, y, Reports.displayMaxDataLengthFromCustomer(str(customer[2])))
            customer_canvas.drawString(x + 130, y, Reports.displayMaxDataLengthFromCustomer(str(customer[3])))
            customer_canvas.drawString(x + 190, y, Reports.displayMaxDataLengthFromCustomer(str(customer[5])))
            customer_canvas.drawString(x + 270, y, Reports.displayMaxDataLengthFromCustomer(str(customer[8])))
            customer_canvas.drawString(x + 350, y, Reports.displayMaxDataLengthFromCustomer(str(customer[9])))
            customer_canvas.drawString(x + 430, y, Reports._displayHumanReadHistorical(customer[10]))

            y -= 25

    @staticmethod
    def _displayHumanReadHistorical(historical):
        if bool(historical):
            return "Active"
        else:
            return "Inactive"

    @staticmethod
    def footer(customer_canvas, title):
        try:
            customer_canvas.line(35, 50, 525, 50)
            today = datetime.datetime.today()
            displayToday = today.strftime("%d/%m/%Y %H:%M:%S")
            customer_canvas.setFont("Helvetica", 7)
            customer_canvas.drawString(45, 40, displayToday)
            customer_canvas.drawString(250,40, title)
            customer_canvas.drawString(450, 40, "Page: " + str(customer_canvas.getPageNumber()))
        except Exception as e:
            print(f"Error en Reports footer: {e}" )

    @staticmethod
    def topHeaderReport(canvas, title):
        try:
            logo_path = ".\\img\\gabrielgsd.jpg"
            logo = Image.open(logo_path)

            if not isinstance(logo, Image.Image):
                print("Error en logo: " + str(logo_path))
                return

            Reports.displayBusinessData(canvas)

            # Draw square for business Data
            canvas.line(20, 800, 120, 800)
            canvas.line(20, 700, 120, 700)

            canvas.line(20, 700, 20, 800)
            canvas.line(120, 700, 120, 800)

            canvas.setFont("Helvetica", 10)
            canvas.drawCentredString(55, 785, "Empresa Teis")
            canvas.drawCentredString(300, 675, title)
            canvas.line(35, 665, 525, 665)
            canvas.drawImage(logo_path, 480, 745, width=40, height=40)

        except Exception as e:
            print(f"Error en Reports top header: {e}" )

    @staticmethod
    def displayBusinessData(canvas):
        try:
            canvas.setFont("Helvetica", 9)
            x = 25
            canvas.drawString(x, 755, "CIF: A12345678")
            canvas.drawString(x, 745, "Avda. de Galicia, 101")
            canvas.drawString(x, 735, "Vigo - 36215- España")
            canvas.drawString(x, 725, "Tlfo: 986123456")
            canvas.drawString(x, 715, "email: teis@mail.com")

        except Exception as e:
            print(f"Error en displayBusinessData: {e}" )


    @staticmethod
    def displayColumnDataHeaders(canvas):
        canvas.setFont("Helvetica", 10)
        for i in range(len(Reports.columns_data)):
            x, y = Reports.coords_columns[i]
            canvas.drawString(x, y, str(Reports.columns_data[i]))

        canvas.line(35, 645, 525, 645)

    @staticmethod
    def displayMaxDataLengthFromCustomer(customer_data):
        try:
            MAX_LENGTH = 15
            if len(customer_data) > MAX_LENGTH:
                return customer_data[:MAX_LENGTH] + "..."

            return customer_data

        except Exception as e:
            print(f"Error en displayMaxDataLengthFromCustomer: {e}" )