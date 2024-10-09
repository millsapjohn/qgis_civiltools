from qgis.gui import (
    QgsMapCanvas,
    QgsMapMouseEvent,
    QgsRubberBand,
    QgsMapTool,
)
from qgis.PyQt.QtGui import QKeyEvent, QCursor, QPixmap
from qgis.PyQt.QtCore import Qt, QPoint
from qgis.PyQt.QtWidgets import QLineEdit
from ..resources.cursor_builder import CTCursor
import os

class BaseMapTool(QgsMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        QgsMapTool.__init__(self, self.canvas)
        # TODO get cursor position for cursor bar
        self.validateCursor()
        self.cursor = QCursor(QPixmap(self.cursorpath))
        self.setCursor(self.cursor)
        self.message = ""
        self.last_command = ""
        self.cursor_bar = QLineEdit()
        self.cursor_bar.setParent(self.canvas)
        self.cursor_bar.resize(80, 20)
        self.cursor_bar.move(QPoint((self.canvas.mouseLastXY().x() + 10), (self.canvas.mouseLastXY().y() + 10)))

    def reset(self):
        # clear any messages from child commands, reset base message, hide cursor bar
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage("Drafting Mode", duration=0)
        self.message = ""
        self.cursor_bar.hide()

    def deactivate(self):
        self.message = ""
        self.cursor_bar.hide()
        QgsMapTool.deactivate(self)
        self.deactivated.emit()

    def canvasMoveEvent(self, e):
        self.cursor_bar.move(QPoint((e.pixelPoint().x() + 10), (e.pixelPoint().y() + 10)))
    
    def keyPressEvent(self, e):
        match e.key():
            case Qt.Key_Return:
                self.sendCommand()
            case Qt.Key_Escape:
                self.message = ""
                self.cursor_bar.hide()
            case Qt.Key_Tab:
                # BUG: currently loses focus without sending command
                self.sendCommand()
            case Qt.Key_Space:
                self.sendCommand()
            case Qt.Key_Backspace:
                # BUG: currently attempts to delete features without updating message
                if len(self.message) == 0:
                    pass
                elif len(self.message) == 1:
                    self.message = ""
                    self.cursor_bar.hide()
                else:
                    self.message = self.message[:-1]
                    self.cursor_bar.setText(self.message)
            case _:
                if self.message == "":
                    self.cursor_bar.show()
                self.message = self.message + e.text()
                self.cursor_bar.setText(self.message)

    def sendCommand(self):
        if len(self.message) == 0:
            if self.last_command == "":
                pass
            else:
                self.iface.messageBar().pushMessage(self.last_command)
        else:
            self.iface.messageBar().pushMessage(self.message)
            self.last_command = self.message
            self.message = ""
            self.cursor_bar.hide()

    def validateCursor(self):
        # check for existing cursor image, create new from defaults if not found
        self.filepath = os.path.dirname(os.path.realpath(__file__))
        self.pluginpath = os.path.split(self.filepath)[0]
        self.cursorpath = os.path.join(self.pluginpath, 'resources/cursor.png')
        if os.path.exists(self.cursorpath):
            pass
        else:
            self.new_cursor = CTCursor(6, 100, (0,0,0), self.extension)
            self.new_cursor.drawCursor()
