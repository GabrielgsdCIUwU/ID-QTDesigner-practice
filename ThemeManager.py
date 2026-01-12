import styles

class ThemeManager:
    """
        Manages dynamic stylesheet switching across multiple registered windows.
    """
    def __init__(self):
        """
            Initializes the manager with the current theme from settings.
        """
        self.current_theme = styles.getCurrentStyle()
        self.windows = []

    def register(self, window):
        """
            Adds a window to the list of managed components and applies the current theme.

            :param window: The QWidget or QMainWindow to register.
            :type window: QWidget
        """
        if window not in self.windows:
            self.windows.append(window)
            window.setStyleSheet(styles.load_stylesheet())

    def apply_theme(self):
        """
            Reloads the stylesheet and applies it to all registered windows.
        """
        stylesheet = styles.load_stylesheet()
        for window in self.windows:
            window.setStyleSheet(stylesheet)

    def change_theme(self, new_theme):
        """
            Updates the active theme and triggers a global style refresh.

            :param new_theme: The name of the theme file (without extension).
            :type new_theme: str
        """
        self.current_theme = new_theme
        self.apply_theme()