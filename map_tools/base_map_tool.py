from qgis.gui import (
    QgsMapCanvas,
    QgsMapMouseEvent,
    QgsRubberBand,
    QgsMapTool,
)
from qgis.PyQt.QtGui import QKeyEvent
from qgis.PyQt.QtCore import Qt

class BaseMapTool(QgsMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        QgsMapTool.__init__(self, self.canvas)
        self.message = ""

    def reset(self):
        # clear any messages from child commands, reset base message
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage("Drafting Mode", duration=0)
        self.message = ""

    def deactivate(self):
        self.message = ""
        QgsMapTool.deactivate(self)
        self.deactivated.emit()

    def keyPressEvent(self, e):
        match e.key():
            case Qt.Key_Return:
                self.iface.messageBar().pushMessage(self.message)
                self.message = ""
            case Qt.Key_Escape:
                self.message = ""
            case Qt.Key_Tab:
                self.iface.messageBar().pushMessage(self.message)
                self.message = ""
            case Qt.Key_Backspace:
                self.message = self.message[:-1]
            case _:
                self.message = self.message + e.text()
