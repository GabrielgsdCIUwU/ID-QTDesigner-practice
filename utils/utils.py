import globals
class Utils:
    """
        Collection of reusable UI utility functions.
    """
    @staticmethod
    def clearStyles():
        """
            Resets the inline CSS styles for form validation fields.
        """
        globals.ui.le_dni.setStyleSheet("")
        globals.ui.le_email.setStyleSheet("")
        globals.ui.le_phone.setStyleSheet("")
        globals.ui.lbl_status.setText("")

    @staticmethod
    def disableLineEdit(line_edit):
        """
            Disables a QLineEdit and tracks it for future bulk re-enabling.

            :param line_edit: The widget to disable.
            :type line_edit: QLineEdit
        """
        line_edit.setEnabled(False)
        globals.disabled_line_edits.append(line_edit)

    @staticmethod
    def enableLineEdit(line_edit):
        """
            Enables a QLineEdit and removes it from the tracking list.

            :param line_edit: The widget to enable.
            :type line_edit: QLineEdit
        """
        line_edit.setEnabled(True)
        globals.disabled_line_edits.remove(line_edit)

    @staticmethod
    def enableAllLineEdit():
        """
           Re-enables all widgets currently stored in the disabled tracking list.
       """
        [line_edit.setEnabled(True) for line_edit in globals.disabled_line_edits]
        globals.disabled_line_edits = []