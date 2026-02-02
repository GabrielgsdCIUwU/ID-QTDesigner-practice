import globals
from PyQt6 import  QtCore, QtGui, QtWidgets
class PaginationManager:
    def __init__(self, items_per_page=10):
        """
        Initializes the pagination manager with a specific number of items per page.

        :param items_per_page: Number of records to show in each table page.
        :type items_per_page: int
        """
        self.items_per_page = items_per_page

        self.tab_states = {}
        self.refresh_callbacks = {}
        self.table_names = {}
        self.extra_criteria = {}

        self.lbl_info = QtWidgets.QLabel()

    def register_tab(self, index, table_name, refresh_callback, criteria=None):
        """
        Registers a UI tab into the pagination system.

        :param index: The index of the tab in the QTabWidget.
        :type index: int
        :param table_name: Name of the database table to count records from.
        :type table_name: str
        :param refresh_callback: Function to call when the page changes.
        :type refresh_callback: callable
        :param criteria: Optional SQL WHERE clause for filtering.
        :type criteria: str | None
        """
        self.tab_states[index] = 0
        self.table_names[index] = table_name
        self.refresh_callbacks[index] = refresh_callback
        self.extra_criteria[index] = criteria

    def get_offset(self, index):
        """
        Calculates the SQL OFFSET based on the current page of a tab.

        :param index: The tab index.
        :type index: int
        :return: The number of records to skip.
        :rtype: int
        """
        return self.tab_states.get(index, 0) * self.items_per_page

    def next_page(self):
        """
        Increments the current page for the active tab and refreshes its data.
        """
        index = globals.ui.pan_main.currentIndex()
        if index in self.tab_states:
            total_items = self._get_total(index)
            if (self.tab_states[index] + 1) * self.items_per_page < total_items:
                self.tab_states[index] += 1
                self.refresh_callbacks[index]()
                self.update_labels()

    def previous_page(self):
        """
        Decrements the current page for the active tab and refreshes its data.
        """
        index = globals.ui.pan_main.currentIndex()
        if index in self.tab_states and self.tab_states[index] > 0:
            self.tab_states[index] -= 1
            self.refresh_callbacks[index]()
            self.update_labels()

    def _get_total(self, index):
        """
        Internal method to retrieve the total record count for a specific tab from the database.

        :param index: The tab index in the QTabWidget.
        :type index: int
        :return: Total number of records in the associated table.
        :rtype: int
        """
        from connection import Connection
        return Connection.getTotalCount(self.table_names[index], self.extra_criteria[index])

    def update_labels(self):
        """
        Updates the status bar label with "Page X/Y" information for the current tab.
        """
        index = globals.ui.pan_main.currentIndex()
        if not index in self.tab_states:
            self.lbl_info.setText("")
            return

        total_items = self._get_total(index)
        items_per_page = self.items_per_page
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
        current_page = self.tab_states[index] + 1
        self.lbl_info.setText(f"Page {current_page}/{total_pages}. Total: {total_items}")