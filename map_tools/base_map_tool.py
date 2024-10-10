# TODO: figure out how to clip the cursor to the map canvas without having to constantly redraw the cursor dynamically
# TODO: figure out how to override Tab keyboard shortcut

from qgis.gui import (
    QgsMapCanvas,
    QgsMapMouseEvent,
    QgsRubberBand,
    QgsMapTool,
)
from qgis.PyQt.QtGui import QKeyEvent, QCursor, QPixmap
from qgis.PyQt.QtCore import Qt, QPoint, QEvent
from qgis.PyQt.QtWidgets import QLineEdit, QMenu, QAction
from ..resources.cursor_builder import CTCursor
from .context_menus import baseContextMenu
import os

class BaseMapTool(QgsMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        QgsMapTool.__init__(self, self.canvas)
        self.flags()
        self.validateCursor()
        self.cursor = QCursor(QPixmap(self.cursorpath))
        self.setCursor(self.cursor)
        self.message = ""
        self.last_command = ""
        self.cursor_bar = QLineEdit()
        self.cursor_bar.setParent(self.canvas)
        self.cursor_bar.resize(80, 20)
        self.cursor_bar.move(QPoint((self.canvas.mouseLastXY().x() + 10), (self.canvas.mouseLastXY().y() + 10)))

    def populateContextMenu(self, menu):
        self.context_menu = baseContextMenu(menu)

    def flags(self):
        return super().flags() | QgsMapTool.ShowContextMenu
    
    def reset(self):
        # clear any messages from child commands, reset base message, hide cursor bar
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage("Drafting Mode", duration=0)
        self.message = ""
        self.cursor_bar.hide()
        self.canvas.contextMenuAboutToShow.disconnect(self.populateContextMenu)

    def deactivate(self):
        self.message = ""
        self.cursor_bar.hide()
        QgsMapTool.deactivate(self)
        self.deactivated.emit()

    def canvasMoveEvent(self, e):
        self.cursor_bar.move(QPoint((e.pixelPoint().x() + 10), (e.pixelPoint().y() + 10)))
    
    def keyPressEvent(self, e):
        e.ignore()
        match e.key():
            case Qt.Key_Return:
                self.sendCommand()
            case Qt.Key_Enter:
                self.sendCommand()
            case Qt.Key_Escape:
                self.message = ""
                self.cursor_bar.hide()
            case Qt.Key_Space:
                self.sendCommand()
            case Qt.Key_Backspace:
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
