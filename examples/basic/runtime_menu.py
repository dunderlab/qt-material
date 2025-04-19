from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from qt_material import QtStyleTools
import os


########################################################################
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'assets', 'main_window.ui')
        self.main = QUiLoader().load(ui_path, self)

        self.add_menu_theme(self.main, self.main.menuStyles)


if __name__ == "__main__":
    app = QApplication()
    frame = RuntimeStylesheets()
    frame.main.show()
    app.exec()
