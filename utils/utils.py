import globals
class Utils:
    @staticmethod
    def clearStyles():
        globals.ui.le_dni.setStyleSheet("")
        globals.ui.le_email.setStyleSheet("")
        globals.ui.le_phone.setStyleSheet("")
        globals.ui.lbl_status.setText("")

    @staticmethod
    def disableLineEdit(line_edit):
        line_edit.setEnabled(False)
        globals.disabled_line_edits.append(line_edit)

    @staticmethod
    def enableLineEdit(line_edit):
        line_edit.setEnabled(True)
        globals.disabled_line_edits.remove(line_edit)

    @staticmethod
    def enableAllLineEdit():
        [line_edit.setEnabled(True) for line_edit in globals.disabled_line_edits]
        globals.disabled_line_edits = []