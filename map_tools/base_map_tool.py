# TODO: figure out how to override Tab keyboard shortcut

from qgis.gui import (
    QgsRubberBand,
    QgsMapTool,
)
from qgis.PyQt.QtGui import QColor, QCursor, QAction
from qgis.PyQt.QtCore import Qt, QPoint
from qgis.PyQt.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsRectangle,
    QgsSettings,
    QgsLineString,
    QgsPoint,
    QgsGeometry,
    Qgis,
)
from .context_menus import baseContextMenu
from .key_validator import keyValidator


class BaseMapTool(QgsMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        # delete shortcuts before reinitializing
        self.bsp_action = None
        self.arrow_down_action = None
        self.arrow_up_action = None
        self.hint_selected = None
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
        self.hint_selected = None
        self.vlayers = []  # list of visible vector layers in the project
        self.non_cad_layers = [] # list of visible non-CAD layers in the project (for style override)
        self.getVectorLayers()
        for entry in self.non_cad_layers:
            if entry[0].geometryType() == Qgis.GeometryType.Point:
                entry[0].renderer().symbol().setColor(self.point_color)
                entry[0].triggerRepaint()
            elif entry[0].geometryType() == Qgis.GeometryType.Line:
                entry[0].renderer().symbol().setColor(self.line_color)
                entry[0].triggerRepaint()
            elif entry[0].geometryType() == Qgis.GeometryType.Polygon:
                entry[0].renderer().symbol().setColor(self.polygon_color)
                entry[0].triggerRepaint()
        self.selfeatures = []  # list of selected features and their layer
        self.sellayers = []  # list of layers that currently have a feature selected
        self.cursor_bar = QLineEdit()
        self.hint_table = QTableWidget()
        self.hint_table.setColumnCount(2)
        self.hint_table.setFixedHeight(124)
        self.hint_table.setFixedWidth(236)
        self.hint_table.verticalHeader().setVisible(False)
        self.hint_table.horizontalHeader().setVisible(False)
        self.hint_table.setParent(self.canvas)
        self.hint_table.move(
            QPoint(
                (self.canvas.mouseLastXY().x() + 90),
                (self.canvas.mouseLastXY().y() + 10),
            )
        )
        self.cursor_bar.setParent(self.canvas)
        self.cursor_bar.resize(80, 20)
        self.cursor_bar.move(
            QPoint(
                (self.canvas.mouseLastXY().x() + 10),
                (self.canvas.mouseLastXY().y() + 10),
            )
        )
        # reinitialize shortcuts
        if not self.bsp_action:
            self.bsp_action = QAction(self.canvas)
            self.bsp_action.setShortcut(Qt.Key_Backspace)
            self.bsp_action.triggered.connect(self.handleBackspace)
            self.canvas.addAction(self.bsp_action)
        elif self.bsp_action not in self.canvas.actions():
            self.canvas.addAction(self.bsp_action)        
        if not self.arrow_down_action:
            self.arrow_down_action = QAction(self.canvas)
            self.arrow_down_action.setShortcut(Qt.Key_Down)
            self.arrow_down_action.triggered.connect(self.handleDownArrow)
            self.canvas.addAction(self.arrow_down_action)
        elif self.arrow_down_action not in self.canvas.actions():
            self.canvas.addAction(self.arrow_down_action)
        if not self.arrow_up_action:
            self.arrow_up_action = QAction(self.canvas)
            self.arrow_up_action.setShortcut(Qt.Key_Up)
            self.arrow_up_action.triggered.connect(self.handleUpArrow)
            self.canvas.addAction(self.arrow_up_action)
        elif self.arrow_up_action not in self.canvas.actions():
            self.canvas.addAction(self.arrow_up_action)
                    
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
        self.hint_table.hide()
        self.icon.reset()
        # TODO: figure out why this is throwing errors
        # self.canvas.contextMenuAboutToShow.disconnect(self.populateContextMenu)

    def deactivate(self):
        if self.bsp_action and self.bsp_action in self.canvas.actions():
            self.bsp_action.triggered.disconnect(self.handleBackspace)
            self.canvas.removeAction(self.bsp_action)
        if self.arrow_down_action and self.arrow_down_action in self.canvas.actions():
            self.arrow_down_action.triggered.disconnect(self.handleDownArrow)
            self.canvas.removeAction(self.arrow_down_action)
        if self.arrow_up_action and self.arrow_up_action in self.canvas.actions():
            self.arrow_up_action.triggered.disconnect(self.handleUpArrow)
            self.canvas.removeAction(self.arrow_up_action)
        self.message = ""
        self.vlayers = []
        for entry in self.non_cad_layers:
            entry[0].renderer().symbol().setColor(entry[1])
            entry[0].triggerRepaint()
        self.non_cad_layers = []
        self.clearSelected()
        self.cursor_bar.hide()
        self.hint_table.hide()
        self.hint_selected = None
        self.icon.reset()
        self.canvas.setCanvasColor(QgsProject.instance().backgroundColor())
        QgsMapTool.deactivate(self)
        self.deactivated.emit()

    def canvasMoveEvent(self, e):
        self.drawCursor(self.canvas, self.icon, e.pixelPoint().x(), e.pixelPoint().y())
        self.hint_table.move(
            QPoint(
                (e.pixelPoint().x() + 90),
                (e.pixelPoint().y() + 10)
            )
        )
        self.cursor_bar.move(
            QPoint((e.pixelPoint().x() + 10), (e.pixelPoint().y() + 10))
        )

    def keyPressEvent(self, e):
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
                    self.hint_table.hide()
            case Qt.Key_Space:
                self.sendCommand()
            case Qt.Key_Shift:
                pass
            case Qt.Key_Control:
                pass
            case _:
                if self.message == "":
                    self.cursor_bar.show()
                self.message = self.message + e.text().upper()
                self.cursor_bar.setText(self.message)
                self.drawHints()

    def handleBackspace(self):
        if len(self.message) == 0:
            self.reset()
        elif len(self.message) == 1:
            self.message = ""
            self.cursor_bar.hide()
            self.hint_table.hide()
        else:
            self.message = self.message[:-1]
            self.cursor_bar.setText(self.message)
            self.drawHints()

    def handleUpArrow(self):
        if self.hint_table.isHidden == True:
            pass
        elif self.no_matches == 0:
            pass
        elif self.no_matches == 1:
            self.hint_table.item(0, 0).setSelected(True)
            self.hint_table.item(0, 1).setSelected(True)
            self.hint_selected = 0
            self.message = self.hint_table.item(0, 0).text()
            self.cursor_bar.setText(self.message)
        else:
            if self.hint_selected == None:
                self.hint_selected = 0
            else:
                raw_hint = self.hint_selected - 1
                if raw_hint < 0:
                    self.hint_selected = self.no_matches - 1
                else:
                    self.hint_selected = raw_hint
            for i in range(self.no_matches):
                self.hint_table.item(i, 0).setSelected(False)
                self.hint_table.item(i, 1).setSelected(False)
            self.hint_table.item(self.hint_selected, 0).setSelected(True)
            self.hint_table.item(self.hint_selected, 1).setSelected(True)
            self.message = self.hint_table.item(self.hint_selected, 0).text()
            self.cursor_bar.setText(self.message)

    def handleDownArrow(self):
        if self.hint_table.isHidden == True:
            pass
        elif self.no_matches == 0:
            pass
        elif self.no_matches == 1:
            self.hint_table.item(0, 0).setSelected(True)
            self.hint_table.item(0, 1).setSelected(True)
            self.hint_selected = 0
            self.message = self.hint_table.item(0, 0).text()
            self.cursor_bar.setText(self.message)
        else:
            if self.hint_selected == None:
                self.hint_selected = 0
            else:
                raw_hint = self.hint_selected + 1
                if raw_hint >= self.no_matches:
                    self.hint_selected = 0
                else:
                    self.hint_selected = raw_hint
            for i in range(self.no_matches):
                self.hint_table.item(i, 0).setSelected(False)
                self.hint_table.item(i, 1).setSelected(False)
            self.hint_table.item(self.hint_selected, 0).setSelected(True)
            self.hint_table.item(self.hint_selected, 1).setSelected(True)
            self.message = self.hint_table.item(self.hint_selected, 0).text()
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

    def drawHints(self):
        self.hint_table.clearContents()
        self.matches = self.matchCommand(self.message)
        self.no_matches = len(self.matches)
        self.hint_table.setRowCount(self.no_matches)
        for i in range(self.no_matches):
            self.hint_table.setItem(i, 0, QTableWidgetItem(self.matches[i][0]))
            self.hint_table.setItem(i, 1, QTableWidgetItem(self.matches[i][1]))
        self.hint_table.resizeColumnToContents(0)
        self.hint_table.resizeColumnToContents(1)
        self.hint_selected = None
        self.hint_table.show()

    def matchCommand(self, str):
        result = keyValidator(str)
        if result[0] == False:
            matches = []
        else:
            matches = result[1]
        return matches

    def sendCommand(self):
        if len(self.message) == 0:
            if self.last_command == "":
                pass
            else:
                self.iface.messageBar().pushMessage(self.last_command)
        else:
            matches = self.matchCommand(self.message)
            self.iface.messageBar().pushMessage(str(matches))
            self.last_command = self.message
            self.message = ""
            self.cursor_bar.hide()
            self.hint_table.hide()

    def getVectorLayers(self):
        # convenience function for when we start dealing with snaps
        for layer in QgsProject.instance().layerTreeRoot().findLayers():
            if layer.isVisible() and isinstance(layer.layer(), QgsVectorLayer):
                if layer.layer().geometryType() != Qgis.GeometryType.Null:
                    self.vlayers.append(layer.layer().source())
                    if "cad" not in layer.layer().name():
                        color = layer.layer().renderer().symbol().color()
                        self.non_cad_layers.append([layer.layer(), color])

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
