import datetime

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
            date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            root_path = ".\\data\\reports\\"
            report_name = f"{date}_customers.pdf"

            all_customers_data = Connection.getCustomers(False)

            pdf_path = os.path.join(root_path, report_name)
            customer_canvas = canvas.Canvas(pdf_path)

            for i in range(len(Reports.columns_data)):
                x, y = Reports.coords_columns[i]
                customer_canvas.drawString(x, y, str(Reports.columns_data[i]))

            customer_canvas.line(35, 645, 525, 645)

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
                print("dentro")
                customer_canvas.setFont("Helvetica-Oblique", 8)
                customer_canvas.drawString(450, 75, "Página siguiente...")
                customer_canvas.showPage()

                customer_canvas.setFont("Helvetica", 10)



            customer_canvas.setFont("Helvetica", 8)

            # Data from customers to display
            dni = "****" + str(customer[0][4:7] + "****")
            customer_canvas.drawString(x - 7, y, dni)
            customer_canvas.drawString(x + 50, y, str(customer[2]))
            customer_canvas.drawString(x + 130, y, str(customer[3]))
            customer_canvas.drawString(x + 190, y, str(customer[5]))
            customer_canvas.drawString(x + 270, y, str(customer[8]))
            customer_canvas.drawString(x + 350, y, str(customer[9]))
            customer_canvas.drawString(x + 430, y, Reports._displayHumanReadHistorical(customer[10]))

            y -= 25

    @staticmethod
    def _displayHumanReadHistorical(historical):
        if bool(historical):
            return "Active"
        else:
            return "Inactive"

    @staticmethod
    def footer(customer_canvas):
        try:
            customer_canvas.line(35, 50, 525, 50)
            today = datetime.date.today()
            displayToday = today.strftime("%d/%m/%Y %H:%M:%S")
            customer_canvas.setFont("Helvetica", 7)
        except Exception as e:
            print(f"Error en Reports footer: {e}" )