from qgis.gui import (
    QgsMapCanvas,
    QgsMapMouseEvent,
    QgsRubberBand,
    QgsMapTool,
)
from qgis.PyQt.QtGui import QKeyEvent
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QLineEdit
from ..resources.cursor_builder import CTCursor

class BaseMapTool(QgsMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        QgsMapTool.__init__(self, self.canvas)
        # TODO validate cursor, set cursor, get cursor position for cursor bar
        self.message = ""
        self.cursor_bar = QLineEdit()
        self.cursor_bar.SetParent(self.iface)

    def reset(self):
        # clear any messages from child commands, reset base message
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage("Drafting Mode", duration=0)
        self.message = ""
        self.cursor_bar.hide()

    def deactivate(self):
        self.message = ""
        QgsMapTool.deactivate(self)
        self.deactivated.emit()

    def canvasMoveEvent(self, e):
        # TODO get cursor position, set cursor bar position
        # self.cursor_bar.move(1, 1)

    def keyPressEvent(self, e):
        match e.key():
            # TODO check length of self.message, show/hide cursor bar based on that
            case Qt.Key_Return:
                self.iface.messageBar().pushMessage(self.message)
                self.message = ""
                self.cursor_bar.hide()
            case Qt.Key_Escape:
                self.message = ""
                self.cursor_bar.hide()
            case Qt.Key_Tab:
                self.iface.messageBar().pushMessage(self.message)
                self.message = ""
            case Qt.Key_Space:
                self.iface.messageBar().pushMessage(self.message)
                self.message = ""
                self.cursor_bar.hide()
            case Qt.Key_Backspace:
                self.message = self.message[:-1]
                self.cursor_bar.setText(self.message)
            case _:
                self.message = self.message + e.text()
                self.cursor_bar.setText(self.message)

    def validateCursor(self):
        # TODO reimplement cursor validation here, but check the correct file location
