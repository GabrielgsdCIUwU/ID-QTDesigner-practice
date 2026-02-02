# EmpresaTeis - Enterprise Management System

**EmpresaTeis** is a robust, cross-platform desktop application designed for streamlined enterprise resource management. Built using the **Python** ecosystem and the **PyQt6** framework, it provides a seamless interface for managing customers, inventory, and financial transactions (invoicing).

The system integrates advanced features such as dynamic PDF generation via **ReportLab**, automated data validation, and a custom pagination engine for high-performance data display.

## Key Features

-   **Customer Management:** Complete CRUD operations with real-time DNI/NIE and email validation.
-   **Inventory Control:** Track stock levels with automated "Low Stock" alerts (visual cues) and family-based categorization.
-   **Advanced Invoicing:** Integrated sales module that automatically calculates subtotals, VAT, and totals, including stock synchronization.
-   **Reporting Engine:** Professional PDF generation for:
    *   Individual sales tickets.
    *   Full customer directories.
    *   Inventory reports (Filtered by low stock or product family).
-   **Data Interchange:** Bulk import/export capabilities using **CSV** and **JSON** formats.
-   **System Tools:**
    *   **Theme Manager:** Instant switching between Dark and Light modes.
    *   **Backup & Restore:** Compressed ZIP-based database recovery system.
    *   **Pagination:** Custom manager to handle large datasets efficiently in UI tables.

## Tech Stack

*   **Language:** Python 3.13
*   **UI Framework:** PyQt6 (Qt 6.10)
*   **Database:** SQLite 3 (handled via `QtSql`)
*   **Reporting:** ReportLab (PDF Engine)
*   **Styles:** QSS (Qt Style Sheets)

## Project Structure

```text
├── data/               # SQLite database, Backups, and Reports
├── img/                # UI icons and business assets
├── styles/             # Dark/Light QSS stylesheets
├── templates/          # .ui files (Qt Designer)
├── utils/              # Reusable UI helpers and validators
├── connection.py       # Database abstraction layer
├── invoice.py          # Billing and Sales logic
├── products.py         # Inventory logic
├── customers.py        # CRM logic
├── reports.py          # PDF Generation logic
├── PaginationManager.py# Custom TableView pagination
└── ThemeManager.py     # Dynamic style switching
```

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git https://github.com/GabrielgsdCIUwU/ID-QTDesigner-practice.git
    cd ID-QTDesigner-practice
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

## Usage Highlights

### **Invoicing Workflow**
Select a customer from the "Customers" tab or search by DNI in the "Invoicing" tab. Add items by their ID; the system will automatically fetch prices and calculate the total. Once saved, the inventory is updated automatically, and a PDF ticket can be generated.

### **Database Maintenance**
Access the **Tools** menu to create a manual backup. The system generates a timestamped `.zip` file of the `bbdd.sqlite`, which can be restored at any time to recover the state of the enterprise.

### **Importing Data**
To populate the system quickly, use the **File > Import** menu.
*   **Customers:** Expects a standard `.csv` with headers.
*   **Products:** Expects a `.json` array containing `id`, `name`, `stock`, `family`, and `price`.