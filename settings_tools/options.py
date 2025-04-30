from qgis.gui import QgsOptionsWidgetFactory, QgsOptionsPageWidget, QgsColorDialog
from qgis.core import QgsSettings, QgsProject
from qgis.utils import iface
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QIntValidator, QColor
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
        self.settings = QgsSettings()
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.ovr_layout = QVBoxLayout()
        self.ovr_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.ovr_layout)
        self.layer_layout = QVBoxLayout()
        self.layer_label = QLabel("Layer Settings")
        self.layer_label.setAlignment(Qt.AlignHCenter)
        self.layer_layout.addWidget(self.layer_label)
        self.default_layer_layout = QHBoxLayout()

        self.ovr_layout.addLayout(self.layer_layout)

        self.cursor_layout = QVBoxLayout()
        self.cursor_label = QLabel("Cursor Settings")
        self.cursor_label.setAlignment(Qt.AlignHCenter)
        self.cursor_layout.addWidget(self.cursor_label)
        self.box_label = QLabel("Cursor Box Size (pixels)")
        self.cursor_layout.addWidget(self.box_label)
        self.box_box = QLineEdit()
        self.box_validator = QIntValidator(0, 50, self)
        self.box_box.setValidator(self.box_validator)
        if self.settings.value("CivilTools/box_size") != None:
            self.box_box.setPlaceholderText(
                str(self.settings.value("CivilTools/box_size"))
            )
        else:
            self.box_box.setPlaceholderText("10")
        self.box_box.setFixedWidth(80)
        self.cursor_layout.addWidget(self.box_box)
        self.crosshair_label = QLabel("Crosshair Size (pixels)")
        self.cursor_layout.addWidget(self.crosshair_label)
        self.crosshair_box = QLineEdit()
        self.crosshair_validator = QIntValidator(0, 10000, self)
        self.crosshair_box.setValidator(self.crosshair_validator)
        if self.settings.value("CivilTools/crosshair_size") != None:
            self.crosshair_box.setPlaceholderText(
                str(self.settings.value("CivilTools/crosshair_size"))
            )
        else:
            self.crosshair_box.setPlaceholderText("1000")
        self.crosshair_box.setFixedWidth(80)
        self.cursor_layout.addWidget(self.crosshair_box)
        self.ovr_layout.addLayout(self.cursor_layout)

        self.background_layout = QVBoxLayout()
        self.background_label = QLabel("Map Background Color")
        self.background_label.setAlignment(Qt.AlignHCenter)
        self.background_layout.addWidget(self.background_label)
        self.bg_select_button = QPushButton("Set Override Color")
        self.bg_select_button.setFixedWidth(120)
        self.bg_select_button.clicked.connect(self.getBgColor)
        self.background_layout.addWidget(self.bg_select_button)
        self.ovr_layout.addLayout(self.background_layout)

    def apply(self):
        if self.box_box.isModified() == True:
            self.box_size = int(self.box_box.text())
            self.settings.setValue("CivilTools/box_size", self.box_size)
        if self.crosshair_box.isModified() == True:
            self.crosshair_size = int(self.crosshair_box.text())
            self.settings.setValue("CivilTools/crosshair_size", self.crosshair_size)

    def getBgColor(self):
        if self.settings.value("CivilTools/bg_color") != None:
            self.bg_color = self.settings.value("CivilTools/bg_color")
        else:
            self.bg_color = QgsProject.instance().backgroundColor()
        self.bg_dialog = QgsColorDialog()
        self.bg_color = self.bg_dialog.getColor(initialColor=self.bg_color, parent=self)
        self.settings.setValue("CivilTools/bg_color", self.bg_color)
