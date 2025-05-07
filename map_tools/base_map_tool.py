# TODO: figure out how to override Tab keyboard shortcut

from qgis.gui import (
    QgsMapCanvas,
    QgsMapMouseEvent,
    QgsRubberBand,
    QgsMapTool,
)
from qgis.PyQt.QtGui import QKeyEvent, QColor, QCursor
from qgis.PyQt.QtCore import Qt, QPoint, QEvent
from qgis.PyQt.QtWidgets import QLineEdit, QMenu, QAction
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsMapLayer,
    QgsRectangle,
    QgsSettings,
    QgsLineString,
    QgsPoint,
    QgsGeometry,
)
from ..resources.cursor_builder import CTCursor
from .context_menus import baseContextMenu
import os


class BaseMapTool(QgsMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        # read a bunch of default settings for colors and sizes
        self.settings = QgsSettings()
        if self.settings.value("CivilTools/box_size") is not None:
            self.box_size_raw = int(self.settings.value("CivilTools/box_size"))
        else:
            self.box_size_raw = 10
        if self.settings.value("CivilTools/crosshair_size") is not None:
            self.crosshair_size_raw = int(
                self.settings.value("CivilTools/crosshair_size")
            )
        else:
            self.crosshair_size_raw = 100
        if self.settings.value("CivilTools/bg_color") is not None:
            self.override_color = self.settings.value("CivilTools/bg_color")
        else:
            self.override_color = QgsProject.instance().backgroundColor()
        if self.settings.value("CivilTools/cursor_color") is not None:
            self.cursor_color = self.settings.value("CivilTools/cursor_color")
        else:
            self.cursor_color = QColor(255, 255, 255)
        if self.settings.value("CivilTools/line_color") is not None:
            self.line_color = self.settings.value("CivilTools/line_color")
        else:
            self.line_color = QColor(255, 255, 255)
        if self.settings.value("CivilTools/point_color") is not None:
            self.point_color = self.settings.value("CivilTools/point_color")
        else:
            self.point_color = QColor(255, 255, 255)
        if self.settings.value("CivilTools/polygon_color") is not None:
            self.polygon_color = self.settings.value("CivilTools/polygon_color")
        else:
            self.polygon_color = QColor(255, 255, 255)
        QgsMapTool.__init__(self, self.canvas)
        # override canvas color in drafting mode
        self.canvas.setCanvasColor(self.override_color)
        self.cursor = QCursor()
        self.cursor.setShape(Qt.BlankCursor)
        self.setCursor(self.cursor)
        self.icon = QgsRubberBand(self.canvas)
        self.icon.setColor(self.cursor_color)
        self.initx = canvas.mouseLastXY().x()
        self.inity = canvas.mouseLastXY().y()
        self.drawCursor(self.canvas, self.icon, self.initx, self.inity)
        self.flags()
        self.message = ""  # string to display next to cursor
        self.last_command = ""
        self.vlayers = []  # list of visible vector layers in the project
        self.getVectorLayers()
        self.selfeatures = []  # list of selected features and their layer
        self.sellayers = []  # list of layers that currently have a feature selected
        self.cursor_bar = QLineEdit()
        self.cursor_bar.setParent(self.canvas)
        self.cursor_bar.resize(80, 20)
        self.cursor_bar.move(
            QPoint(
                (self.canvas.mouseLastXY().x() + 10),
                (self.canvas.mouseLastXY().y() + 10),
            )
        )

    def on_map_tool_set(self, new_tool, old_tool):
        if new_tool == self:
            pass
        else:
            self.reset()

    def populateContextMenu(self, menu):
        self.context_menu = baseContextMenu(menu)

    def flags(self):
        return super().flags() | QgsMapTool.ShowContextMenu

    def reset(self):
        # clear any messages from child commands, reset base message, hide cursor bar
        # clear selection list, disconnect from context menu slot
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage("Drafting Mode", duration=0)
        self.message = ""
        self.selfeatures = []
        self.sellayers = []
        self.cursor_bar.hide()
        self.icon.reset()
        # TODO: figure out why this is throwing errors
        # self.canvas.contextMenuAboutToShow.disconnect(self.populateContextMenu)

    def deactivate(self):
        self.message = ""
        self.vlayers = []
        self.clearSelected()
        self.cursor_bar.hide()
        self.icon.reset()
        self.canvas.setCanvasColor(QgsProject.instance().backgroundColor())
        QgsMapTool.deactivate(self)
        self.deactivated.emit()

    def canvasMoveEvent(self, e):
        self.drawCursor(self.canvas, self.icon, e.pixelPoint().x(), e.pixelPoint().y())
        self.cursor_bar.move(
            QPoint((e.pixelPoint().x() + 10), (e.pixelPoint().y() + 10))
        )

    def keyPressEvent(self, e):
        e.ignore()
        match e.key():
            case Qt.Key_Return:
                self.sendCommand()
            case Qt.Key_Enter:
                self.sendCommand()
            case Qt.Key_Escape:
                if len(self.message) == 0:
                    self.clearSelected()
                else:
                    self.message = ""
                    self.cursor_bar.hide()
            case Qt.Key_Space:
                self.sendCommand()
            case Qt.Key_Backspace:
                if len(self.message) == 0:
                    self.reset()
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

    def clearSelected(self):
        self.order = QgsProject.instance().layerTreeRoot().layerOrder()
        for layer in self.order:
            if layer.source() not in self.vlayers:
                continue
            else:
                ids = layer.selectedFeatureIds()
                for id in ids:
                    layer.deselect(id)
        self.selfeatures = []
        self.sellayers = []

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

    def getVectorLayers(self):
        # convenience function for when we start dealing with snaps
        for layer in QgsProject.instance().layerTreeRoot().findLayers():
            if layer.isVisible() and isinstance(layer.layer(), QgsVectorLayer):
                self.vlayers.append(layer.layer().source())

    def canvasPressEvent(self, event):
        # only select one feature per click
        selected = []
        center = event.mapPoint()
        # TODO: set this so the search radius matches the pickbox
        sel_rect = QgsRectangle(
            (center.x() - 2.0),
            (center.y() - 2.0),
            (center.x() + 2.0),
            (center.y() + 2.0),
        )
        # calling this again so it reflects changes in layer order
        self.order = QgsProject.instance().layerTreeRoot().layerOrder()
        for layer in self.order:
            # if a feature is selected, don't cycle more layers
            if selected != []:
                break
            # do nothing if a non-visible vector layer is clicked
            if layer.source() not in self.vlayers:
                continue
            else:
                layer.selectByRect(sel_rect)
                ids = layer.selectedFeatureIds()
                for id in ids:
                    if [layer.name(), id] in self.selfeatures:
                        continue
                    else:
                        self.selfeatures.append([layer.name(), id])
                        selected = [layer.name(), id]
                        break
            # clearing and reselecting seems to be the least
            # error-prone method
            layer.removeSelection()
            for feature in self.selfeatures:
                if feature[0] != layer.name():
                    continue
                else:
                    layer.select(feature[1])
        if selected != []:
            if selected[0] not in self.sellayers:
                self.sellayers.append(selected[0])

    def drawCursor(self, canvas, icon, pixelx, pixely):
        # method for dynamic drawing of the cursor
        # won't extend beyond map extents
        icon.reset()
        self.extent = canvas.extent()
        self.xmax = self.extent.xMaximum()
        self.xmin = self.extent.xMinimum()
        self.ymax = self.extent.yMaximum()
        self.ymin = self.extent.yMinimum()
        self.factor = canvas.mapUnitsPerPixel()
        self.box_size = self.box_size_raw * self.factor
        self.crosshair_size = self.crosshair_size_raw * self.factor
        self.mapx = (pixelx * self.factor) + self.xmin
        self.mapy = self.ymax - (pixely * self.factor)
        self.map_position = QgsPoint(self.mapx, self.mapy)
        self.box_left = QgsGeometry(
            QgsLineString(
                QgsPoint((self.mapx - self.box_size), (self.mapy - self.box_size)),
                QgsPoint((self.mapx - self.box_size), (self.mapy + self.box_size)),
            )
        )
        self.box_right = QgsGeometry(
            QgsLineString(
                QgsPoint((self.mapx + self.box_size), (self.mapy - self.box_size)),
                QgsPoint((self.mapx + self.box_size), (self.mapy + self.box_size)),
            )
        )
        self.box_top = QgsGeometry(
            QgsLineString(
                QgsPoint((self.mapx - self.box_size), (self.mapy - self.box_size)),
                QgsPoint((self.mapx + self.box_size), (self.mapy - self.box_size)),
            )
        )
        self.box_bot = QgsGeometry(
            QgsLineString(
                QgsPoint((self.mapx - self.box_size), (self.mapy + self.box_size)),
                QgsPoint((self.mapx + self.box_size), (self.mapy + self.box_size)),
            )
        )
        if self.map_position.x() - self.box_size - self.crosshair_size > self.xmin:
            self.left_len = self.crosshair_size
        else:
            self.left_len = self.map_position.x() - self.box_size - self.xmin
        if self.map_position.x() + self.box_size + self.crosshair_size < self.xmax:
            self.right_len = self.crosshair_size
        else:
            self.right_len = self.xmax - self.box_size - self.map_position.x()
        if self.map_position.y() - self.box_size - self.crosshair_size > self.ymin:
            self.down_len = self.crosshair_size
        else:
            self.down_len = self.map_position.y() - self.box_size - self.ymin
        if self.map_position.y() + self.box_size + self.crosshair_size < self.ymax:
            self.up_len = self.crosshair_size
        else:
            self.up_len = self.ymax - self.box_size - self.map_position.y()
        self.left_start = QgsPoint(
            (self.map_position.x() - self.box_size), self.map_position.y()
        )
        self.left_end = QgsPoint(
            (self.map_position.x() - self.box_size - self.left_len),
            self.map_position.y(),
        )
        self.left_line = QgsGeometry(QgsLineString(self.left_end, self.left_start))
        self.right_start = QgsPoint(
            (self.map_position.x() + self.box_size), self.map_position.y()
        )
        self.right_end = QgsPoint(
            (self.map_position.x() + self.box_size + self.right_len),
            self.map_position.y(),
        )
        self.right_line = QgsGeometry(QgsLineString(self.right_start, self.right_end))
        self.up_start = QgsPoint(
            self.map_position.x(), (self.map_position.y() + self.box_size)
        )
        self.up_end = QgsPoint(
            self.map_position.x(), (self.map_position.y() + self.box_size + self.up_len)
        )
        self.up_line = QgsGeometry(QgsLineString(self.up_start, self.up_end))
        self.down_start = QgsPoint(
            self.map_position.x(), (self.map_position.y() - self.box_size)
        )
        self.down_end = QgsPoint(
            self.map_position.x(),
            (self.map_position.y() - self.box_size - self.down_len),
        )
        self.down_line = QgsGeometry(QgsLineString(self.down_start, self.down_end))
        icon.addGeometry(self.box_left, doUpdate=False)
        icon.addGeometry(self.box_right, doUpdate=False)
        icon.addGeometry(self.box_top, doUpdate=False)
        icon.addGeometry(self.box_bot, doUpdate=False)
        icon.addGeometry(self.left_line, doUpdate=False)
        icon.addGeometry(self.right_line, doUpdate=False)
        icon.addGeometry(self.up_line, doUpdate=False)
        icon.addGeometry(self.down_line)
