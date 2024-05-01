from qgis.gui import QgsOptionsWidgetFactory, QgsOptionsPageWidget
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
                                QHBoxLayout,
                                QVBoxLayout,
                                QLabel,
                                QListWidget,
                                QDialog,
                                QCheckBox,
                                )


class CivilToolsOptionsFactory(QgsOptionsWidgetFactory):
    def __init__(self):
        super().__init__()

    def icon(self):
        return QIcon(":/images/themes/default/cadtools/cad.svg")

    def createWidget(self, parent):
        return CivilToolsConfigOptionsPage(parent)


class CivilToolsConfigOptionsPage(QgsOptionsPageWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ovr_layout = QVBoxLayout()
        self.ovr_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.ovr_layout)
        self.layer_layout = QVBoxLayout()
        self.layer_label = QLabel("Layer Settings")
        self.layer_layout.addWidget(self.layer_label)
        self.default_layer_layout = QHBoxLayout()

        self.ovr_layout.addLayout(self.layer_layout)
