# TODO: figure out how to override Tab keyboard shortcut

from qgis.gui import QgsRubberBand
from qgis.PyQt.QtGui import QColor, QAction
from qgis.PyQt.QtCore import Qt
from qgis.core import (
    QgsProject,
    QgsRectangle,
    QgsGeometry,
    Qgis,
)
from .context_menus import baseContextMenu
from .base_map_tool import BaseMapTool


class SelectMapTool(BaseMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        # delete shortcuts before reinitializing
        self.is_dragging = False
        self.is_tracing = False
        self.sel_band = QgsRubberBand(self.canvas)
        self.poly_sel_band = QgsRubberBand(self.canvas)
        # TODO: make this a setting
        self.sel_band.setStrokeColor(QColor(0, 18, 255))
        self.poly_sel_band.setStrokeColor(QColor(0, 18, 255))
        BaseMapTool.__init__(self, self.canvas)
        self.selfeatures = []  # list of selected features and their layer
        self.sellayers = []  # list of layers that currently have a feature selected

    def on_map_tool_set(self, new_tool, old_tool):
        if new_tool == self:
            pass
        else:
            self.reset()

    def populateContextMenu(self, menu):
        self.context_menu = baseContextMenu(menu)

    def flags(self):
        return super().flags() | BaseMapTool.ShowContextMenu

    def reset(self):
        BaseMapTool.reset()
        self.selfeatures = []
        self.sellayers = []
        self.is_dragged = False
        self.is_tracing = False
        self.clearSelected()
        self.sel_band.reset()
        self.poly_sel_band.reset()
        # TODO: figure out why this is throwing errors
        # self.canvas.contextMenuAboutToShow.disconnect(self.populateContextMenu)

    def deactivate(self):
        self.clearSelected()
        BaseMapTool.deactivate(self)
        self.deactivated.emit()

    def canvasMoveEvent(self, e):
        BaseMapTool.canvasMoveEvent(e)
        if self.is_dragging is True:
            self.drawSelector(self.first_loc, e.mapPoint())
        elif self.is_tracing is True:
            self.drawPolySelector(e.mapPoint())

    def keyPressEvent(self, e):
        match e.key():
            case Qt.Key_Return:
                self.sendCommand()
            case Qt.Key_Enter:
                self.sendCommand()
            case Qt.Key_Escape:
                if len(self.message) == 0:
                    if self.is_dragging is True:
                        self.is_dragging = False
                        self.sel_band.reset()
                    elif self.is_tracing is True:
                        self.is_tracing = False
                        self.poly_sel_band.reset()
                    else:
                        self.clearSelected()
                else:
                    self.message = ""
                    self.cursor_bar.hide()
                    self.hint_table.hide()
            case Qt.Key_Space:
                self.sendCommand()
            case Qt.Key_Shift:
                self.shift_modified = True
            case Qt.Key_Control:
                self.ctrl_modified = True
            case _:
                if self.message == "":
                    self.cursor_bar.show()
                self.message = self.message + e.text().upper()
                self.cursor_bar.setText(self.message)
                self.drawHints()

    def keyReleaseEvent(self, e):
        BaseMapTool.keyReleaseEvent(e)

    def clearSelected(self):
        self.iface.mainWindow().findChild(QAction, 'mActionDeselectAll').trigger()
        self.selfeatures = []
        self.sellayers = []

    def canvasPressEvent(self, event):
        self.press_success = False
        self.first_loc = event.mapPoint()
        self.first_loc_pixel = event.pixelPoint()
        self.order = QgsProject.instance().layerTreeRoot().layerOrder()
        if not self.is_tracing:
            sel_rect = QgsRectangle(
                (event.mapPoint().x() - (self.box_size_raw / 2)),
                (event.mapPoint().y() - (self.box_size_raw / 2)),
                (event.mapPoint().x() + (self.box_size_raw / 2)),
                (event.mapPoint().y() + (self.box_size_raw / 2))
            )
            sel_geom = QgsGeometry.fromRect(sel_rect)
            sel_engine = QgsGeometry.createGeometryEngine(sel_geom.constGet())
            sel_engine.prepareGeometry()
            if self.shift_modified:
                result = self.deselectOne(self.order, sel_engine)
            else:
                result = self.selectOne(self.order, sel_engine)
            if not result:
                self.is_tracing = True
            else:
                self.press_success = True
        else:
            pass

    def canvasReleaseEvent(self, event):
        self.second_loc = event.mapPoint()
        self.second_loc_pixel = event.pixelPoint()
        if self.press_success is True:
            pass
        elif self.second_loc == self.first_loc and self.is_dragging is False:
            self.is_tracing = False
            self.is_dragging = True
            self.press_success = False
        elif self.second_loc == self.first_loc and self.is_dragging is True:
            self.is_dragging = False
            self.is_tracing = False
            self.press_success = False
            sel_geom = self.sel_band.asGeometry()
            sel_engine = QgsGeometry.createGeometryEngine(sel_geom.constGet())
            sel_engine.prepareGeometry()
            if self.second_loc_pixel.x() > self.first_loc_pixel.x():
                if self.shift_modified:
                    self.rightDeselect(self.order, sel_engine)
                else:
                    self.rightSelect(self.order, sel_engine)
            else:
                if self.shift_modified:
                    self.leftDeselect(self.order, sel_engine)
                else:
                    self.leftSelect(self.order, sel_engine)
            self.sel_band.reset()
        elif self.is_tracing:
            self.is_tracing = False
            self.press_success = False
            self.poly_sel_band.addPoint(self.second_loc)
            sel_geom = self.poly_sel_band.asGeometry()
            sel_engine = QgsGeometry.createGeometryEngine(sel_geom.constGet())
            sel_engine.prepareGeometry()
            if self.second_loc_pixel.x() > self.first_loc_pixel.x():
                if self.shift_modified:
                    self.rightDeselect(self.order, sel_engine)
                else:
                    self.rightSelect(self.order, sel_engine)
            else:
                if self.shift_modified:
                    self.leftDeselect(self.order, sel_engine)
                else:
                    self.leftSelect(self.order, sel_engine)
            self.poly_sel_band.reset()
        else:
            pass

    def rightSelect(self, order, engine):
        for layer in order:
            if layer.source() not in self.vlayers:
                continue
            else:
                for feature in layer.getFeatures():
                    geom = feature.geometry()
                    if engine.contains(geom.constGet()):
                        if [layer, feature.id()] not in self.selfeatures:
                            layer.selectByIds(
                                [feature.id()],
                                Qgis.SelectBehavior.AddToSelection
                            )
                            self.selfeatures.append([layer, feature.id()])
                            if layer not in self.sellayers:
                                self.sellayers.append(layer)

    def rightDeselect(self, order, engine):
        for layer in order:
            if layer.source() not in self.vlayers:
                continue
            else:
                for feature in layer.getFeatures():
                    geom = feature.geometry()
                    if engine.contains(geom.constGet()):
                        if [layer, feature.id()] in self.selfeatures:
                            layer.deselect(feature.id())
                            self.selfeatures.remove([layer, feature.id()])
                            if layer not in [x[0] for x in self.selfeatures]:
                                self.sellayers.remove(layer)

    def leftDeselect(self, order, engine):
        for layer in order:
            if layer.source() not in self.vlayers:
                continue
            else:
                for feature in layer.getFeatures():
                    geom = feature.geometry()
                    if engine.intersects(geom.constGet()) or engine.contains(geom.constGet()):
                        if [layer, feature.id()] in self.selfeatures:
                            layer.deselect(feature.id())
                            self.selfeatures.remove([layer, feature.id()])
                            if layer not in [x[0] for x in self.selfeatures]:
                                self.sellayers.remove(layer)

    def leftSelect(self, order, engine):
        for layer in order:
            if layer.source() not in self.vlayers:
                continue
            else:
                for feature in layer.getFeatures():
                    geom = feature.geometry()
                    if engine.intersects(geom.constGet()) or engine.contains(geom.constGet()):
                        if [layer, feature.id()] not in self.selfeatures:
                            layer.selectByIds(
                                [feature.id()],
                                Qgis.SelectBehavior.AddToSelection
                            )
                            self.selfeatures.append([layer, feature.id()])
                            if layer not in self.sellayers:
                                self.sellayers.append(layer)

    def selectOne(self, order, engine):
        selected = []
        for layer in order:
            if selected != []:
                break
            if layer.source() not in self.vlayers:
                continue
            else:
                for feature in layer.getFeatures():
                    if selected != []:
                        break
                    geom = feature.geometry()
                    if engine.intersects(geom.constGet()):
                        if [layer, feature.id()] not in self.selfeatures:
                            layer.selectByIds(
                                [feature.id()],
                                Qgis.SelectBehavior.AddToSelection
                            )
                            self.selfeatures.append([layer, feature.id()])
                            if layer not in self.sellayers:
                                self.sellayers.append(layer)
                        selected = [layer, feature.id()]
        if selected != []:
            return True
        else:
            return False

    def deselectOne(self, order, engine):
        deselected = []
        for layer in order:
            if deselected != []:
                break
            if layer.source() not in self.vlayers:
                continue
            else:
                for feature in layer.getFeatures():
                    geom = feature.geometry()
                    if (engine.intersects(geom.constGet()) and
                        [layer, feature.id()] in self.selfeatures):
                        layer.deselect(feature.id())
                        self.selfeatures.remove([layer, feature.id()])
                        if layer not in [x[0] for x in self.selfeatures]:
                            self.sellayers.remove(layer)
                        deselected = [layer, feature.id()]
        if deselected != []:
            return True
        else:
            return False

    def drawSelector(self, first_point, second_point):
        self.sel_band.reset()
        self.sel_band.addGeometry(
                        QgsGeometry().
                        fromRect(
                            QgsRectangle(first_point, second_point)))

    def drawPolySelector(self, point):
        self.poly_sel_band.addPoint(point)
