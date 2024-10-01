from qgis.gui import QgsOptionsWidgetFactory, QgsOptionsPageWidget
from qgis.utils import iface
from qgis.PyQt.QtGui import QIcon, QIntValidator
from qgis.PyQt.QtWidgets import (
                                QHBoxLayout,
                                QVBoxLayout,
                                QLabel,
                                QListWidget,
                                QDialog,
                                QCheckBox,
                                QLineEdit,
                                QPushButton,
                                )
import os
from .resources.cursor_builder import CTCursor


class CivilToolsOptionsFactory(QgsOptionsWidgetFactory):
    def __init__(self):
        super().__init__()

    def icon(self):
        return QIcon(":/images/themes/default/cadtools/cad.svg")

    def createWidget(self, parent):
        return CivilToolsConfigOptionsPage(parent)


class CivilToolsConfigOptionsPage(QgsOptionsPageWidget):
    def __init__(self, parent):
        self.iface = iface
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.ovr_layout = QVBoxLayout()
        self.ovr_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.ovr_layout)
        self.layer_layout = QVBoxLayout()
        self.layer_label = QLabel("Layer Settings")
        self.layer_layout.addWidget(self.layer_label)
        self.default_layer_layout = QHBoxLayout()

        self.ovr_layout.addLayout(self.layer_layout)
        
        self.cursor_layout = QHBoxLayout()
        self.cursor_label = QLabel("Cursor Settings")
        self.cursor_layout.addWidget(self.cursor_label)
        self.box_label = QLabel("Cursor Box Size (pixels)")
        self.cursor_layout.addWidget(self.box_label)
        self.box_box = QLineEdit()
        self.box_validator = QIntValidator(0, 50, self)
        self.box_box.setValidator(self.box_validator)
        self.cursor_layout.addWidget(self.box_box)
        self.crosshair_label = QLabel("Crosshair Size (pixels)")
        self.cursor_layout.addWidget(self.crosshair_label)
        self.crosshair_box = QLineEdit()
        self.crosshair_validator = QIntValidator(0, 10000, self)
        self.crosshair_box.setValidator(self.crosshair_validator)
        self.cursor_layout.addWidget(self.crosshair_box)
        self.cursor_button = QPushButton('Apply')
        self.cursor_button.clicked.connect(self.getCursorValues)
        self.cursor_layout.addWidget(self.cursor_button)

        self.ovr_layout.addLayout(self.cursor_layout)

    def getCursorValues(self):
        self.box_size = int(self.box_box.text())
        self.crosshair_size = int(self.crosshair_box.text())
        pluginpath = os.path.dirname(os.path.realpath(__file__))
        extension = os.path.join(pluginpath,'resources\\cursor.jpg')
        new_cursor = CTCursor(self.box_size, self.crosshair_size, (0,0,0), extension)
        new_cursor.drawCursor()
