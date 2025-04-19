from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from qt_material import apply_stylesheet
import os


########################################################################
class ShowUI(QMainWindow):
    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'assets', 'main_window.ui')
        self.main = QUiLoader().load(ui_path, self)


if __name__ == "__main__":
    app = QApplication()

    apply_stylesheet(app, theme='dark_cyan.xml')

    frame = ShowUI()
    frame.main.show()

    app.exec_()
