import globals
from PyQt6 import  QtCore, QtGui, QtWidgets
class PaginationManager:
    def __init__(self, items_per_page=10):
        self.items_per_page = items_per_page

        self.tab_states = {}
        self.refresh_callbacks = {}
        self.table_names = {}
        self.extra_criteria = {}

        self.lbl_info = QtWidgets.QLabel()

    def register_tab(self, index, table_name, refresh_callback, criteria=None):
        self.tab_states[index] = 0
        self.table_names[index] = table_name
        self.refresh_callbacks[index] = refresh_callback
        self.extra_criteria[index] = criteria

    def get_offset(self, index):
        return self.tab_states.get(index, 0) * self.items_per_page

    def next_page(self):
        index = globals.ui.pan_main.currentIndex()
        if index in self.tab_states:
            total_items = self._get_total(index)
            if (self.tab_states[index] + 1) * self.items_per_page < total_items:
                self.tab_states[index] += 1
                self.refresh_callbacks[index]()
                self.update_labels()

    def previous_page(self):
        index = globals.ui.pan_main.currentIndex()
        if index in self.tab_states and self.tab_states[index] > 0:
            self.tab_states[index] -= 1
            self.refresh_callbacks[index]()
            self.update_labels()

    def _get_total(self, index):
        from connection import Connection
        return Connection.getTotalCount(self.table_names[index], self.extra_criteria[index])

    def update_labels(self):
        index = globals.ui.pan_main.currentIndex()
        if not index in self.tab_states:
            self.lbl_info.setText("")
            return

        total_items = self._get_total(index)
        items_per_page = self.items_per_page
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
        current_page = self.tab_states[index] + 1
        self.lbl_info.setText(f"Page {current_page}/{total_pages}. Total: {total_items}")