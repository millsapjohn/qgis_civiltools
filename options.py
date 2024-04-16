from qgis.gui import QgsOptionsWidgetFactory, QgsOptionsPageWidget
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QHBoxLayout

class CivilToolsOptionsFactory(QgsOptionsWidgetFactory):
    def __init__(self):
        super().__init__()

    def icon(self):
        return QIcon(':/images/themes/default/cadtools/cad.svg')

    def createWidget(self, parent):
        return CivilToolsConfigOptionsPage(parent)

class CivilToolsConfigOptionsPage(QgsOptionsPageWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
