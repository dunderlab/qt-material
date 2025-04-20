import os
import sys
import logging
from multiprocessing import freeze_support

if "--pyside6" in sys.argv:
    from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
    from PySide6.QtCore import QTimer, Qt, QCoreApplication, QEvent
    from PySide6.QtGui import QIcon, QPixmap
    from PySide6.QtUiTools import QUiLoader

elif "--pyqt6" in sys.argv:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
    from PyQt6.QtCore import QTimer, Qt, QCoreApplication
    from PyQt6.QtGui import QIcon
    from PyQt6 import uic, QtWebEngineWidgets

else:
    logging.error("must include --pyside6 or --pyqt6 in args!")

from qt_material import apply_stylesheet, QtStyleTools, density

if hasattr(Qt, "AA_ShareOpenGLContexts"):
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
else:
    print("'Qt' object has no attribute 'AA_ShareOpenGLContexts'")

app = QApplication(sys.argv)
freeze_support()

app.processEvents()
# app.setQuitOnLastWindowClosed(True)
# app.lastWindowClosed.connect(app.quit)

# Extra stylesheets
extra = {
    # Button colors
    "danger": "#dc3545",
    "warning": "#ffc107",
    "success": "#17a2b8",
    # Font
    "font_family": "Roboto",
    # Density
    "density_scale": "0",
    # Button Shape
    "button_shape": "default",
}


########################################################################
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super().__init__()

        if "--pyside6" in sys.argv:
            self.main = QUiLoader().load("main_window.ui", self)
            self.main.installEventFilter(self)
            wt = "PySide6"

        elif "--pyqt6" in sys.argv:
            self.main = uic.loadUi("main_window.ui", self)
            wt = "PyQt6"

        self.main.setWindowTitle(f"{self.main.windowTitle()} - {wt}")

        self.custom_styles()
        self.set_extra(extra)
        self.add_menu_density(self, self.main.menuDensity)
        self.add_menu_theme(self, self.main.menuStyles)
        self.show_dock_theme(self)

        logo = QIcon("qt_material:/logo/logo.svg")
        logo_frame = QIcon("qt_material:/logo/logo_frame.svg")

        self.setWindowIcon(logo)
        self.main.actionToolbar.setIcon(logo)

        for i in range(self.main.listWidget_2.count()):
            self.main.listWidget_2.item(i).setIcon(logo_frame)

        self.main.pushButton_file_dialog.clicked.connect(
            lambda: QFileDialog.getOpenFileName(self)
        )
        self.main.pushButton_folder_dialog.clicked.connect(
            lambda: QFileDialog.getExistingDirectory(self)
        )

        self.resize(1200, 800)

    # ----------------------------------------------------------------------
    def eventFilter(self, obj, event):
        """"""
        if obj == self.main and event.type() == QEvent.Close:
            print(event)
            QApplication.quit()
            return False
        return super().eventFilter(obj, event)

    # ----------------------------------------------------------------------
    def custom_styles(self):
        """"""
        for i in range(self.main.toolBar_vertical.layout().count()):
            tool_button = self.main.toolBar_vertical.layout().itemAt(i).widget()
            tool_button.setMaximumWidth(150)
            tool_button.setMinimumWidth(150)

        for r in range(self.main.tableWidget.rowCount()):
            self.main.tableWidget.setRowHeight(r, 36)

        for r in range(self.main.tableWidget_2.rowCount()):
            self.main.tableWidget_2.setRowHeight(r, 36)


T0 = 1000

if __name__ == "__main__":

    # ----------------------------------------------------------------------
    def take_screenshot():
        pixmap = frame.main.grab()
        pixmap.save(os.path.join("screenshots", f"{theme}.png"))
        print(f"Saving {theme}")

    if len(sys.argv) > 2:
        theme = sys.argv[2]
        QTimer.singleShot(T0, take_screenshot)
        QTimer.singleShot(T0 * 2, app.closeAllWindows)
    else:
        theme = "default"

    # Set theme on in itialization
    apply_stylesheet(
        app,
        theme + ".xml",
        invert_secondary=("light" in theme and "dark" not in theme),
        extra=extra,
    )

    frame = RuntimeStylesheets()
    frame.main.show()
    app.exec()
