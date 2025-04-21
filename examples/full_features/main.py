import os
import sys
import json
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
            self.main = QUiLoader().load("main_window_v2.ui", self)
            self.main.installEventFilter(self)
            wt = "PySide6"

        elif "--pyqt6" in sys.argv:
            self.main = uic.loadUi("main_window_v2.ui", self)
            wt = "PyQt6"

        self.main.setWindowTitle(f"{self.main.windowTitle()} - {wt}")

        self.set_extra(extra)
        self.register_mdi_areas(self.main.mdiArea)
        self.add_menu_density(self, self.main.menuDensity)
        self.add_menu_theme(self, self.main.menuStyles)
        self.show_dock_theme(self.main)
        self.custom_styles()

        logo = QIcon("qt_material:/logo/logo.svg")
        logo_frame = QIcon("qt_material:/logo/logo_frame.svg")

        self.setWindowIcon(logo)
        self.main.actionToolbar.setIcon(logo)

        for i in range(self.main.listWidget_2.count()):
            self.main.listWidget_2.item(i).setIcon(logo_frame)

        for i in range(self.main.listWidget_3.count()):
            self.main.listWidget_3.item(i).setIcon(logo_frame)

        self.main.pushButton_file_dialog.clicked.connect(
            lambda: QFileDialog.getOpenFileName(self)
        )
        self.main.pushButton_folder_dialog.clicked.connect(
            lambda: QFileDialog.getExistingDirectory(self)
        )

        self.main.action_widgets.triggered.connect(
            lambda: (
                self.main.stackedWidget.setCurrentIndex(0),
                self.main.action_tabs.setChecked(False),
                self.main.action_widgets.setChecked(True),
                self.main.action_examples.setChecked(False),
            )
        )

        self.main.action_tabs.triggered.connect(
            lambda: (
                self.main.stackedWidget.setCurrentIndex(1),
                self.main.action_widgets.setChecked(False),
                self.main.action_tabs.setChecked(True),
                self.main.action_examples.setChecked(False),
            )
        )

        self.main.action_examples.triggered.connect(
            lambda: (
                self.main.stackedWidget.setCurrentIndex(2),
                self.main.action_widgets.setChecked(False),
                self.main.action_tabs.setChecked(False),
                self.main.action_examples.setChecked(True),
                self.save_mdi_subwindow_positions(),
            )
        )

        self.center_window()
        self.load_mdi_subwindow_positions()
        if len(sys.argv) > 2:
            self.main.stackedWidget.setCurrentIndex(2)
        else:
            self.main.stackedWidget.setCurrentIndex(0)
        self.main.toolBox.setCurrentIndex(0)

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
        self.dock_theme.setFloating(False)
        self.dock_theme.setMinimumWidth(400)

    # ----------------------------------------------------------------------
    def center_window(self):
        self.main.resize(1925, 1175)
        frame = self.frameGeometry()
        center = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    # ----------------------------------------------------------------------
    def save_mdi_subwindow_positions(self):
        """"""
        positions = {}
        for w in self.main.mdiArea.subWindowList():
            title = w.windowTitle()
            geom = w.geometry()
            positions[title] = {
                "x": geom.x(),
                "y": geom.y(),
                "width": geom.width(),
                "height": geom.height(),
            }
        # Save positions to a JSON file
        with open("mdi_positions.json", "w") as f:
            json.dump(positions, f, indent=4)

    # ----------------------------------------------------------------------
    def load_mdi_subwindow_positions(self):
        """"""
        # Return empty positions if file does not exist
        if not os.path.exists("mdi_positions.json"):
            return {}

        # Load positions from JSON file
        with open("mdi_positions.json", "r") as f:
            positions = json.load(f)
        # Apply saved geometry to each MDI subwindow
        for w in self.main.mdiArea.subWindowList():
            title = w.windowTitle()
            if title in positions:
                pos = positions[title]
                w.setGeometry(pos["x"], pos["y"], pos["width"], pos["height"])
        return positions


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

    apply_stylesheet(
        app,
        theme + ".xml",
        invert_secondary=("light" in theme and "dark" not in theme),
        extra=extra,
    )

    frame = RuntimeStylesheets()

    frame.apply_stylesheet(
        app,
        theme + ".xml",
        invert_secondary=("light" in theme and "dark" not in theme),
        extra=extra,
    )

    frame.main.show()

    app.exec()
