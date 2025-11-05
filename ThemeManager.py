import styles

class ThemeManager:
    def __init__(self):
        self.current_theme = styles.getCurrentStyle()
        self.windows = []

    def register(self, window):
        if window not in self.windows:
            self.windows.append(window)
            window.setStyleSheet(styles.load_stylesheet())

    def apply_theme(self):
        stylesheet = styles.load_stylesheet()
        for window in self.windows:
            window.setStyleSheet(stylesheet)

    def change_theme(self, new_theme):
        self.current_theme = new_theme
        self.apply_theme()