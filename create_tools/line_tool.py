from qgis.core import (
    QgsSnappingUtils,
    QgsPointLocator,
    Qgis,
)
from qgis.gui import QgsRubberBand
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QCursor
from ..map_tools.base_map_tool import BaseMapTool


class LineMapTool(BaseMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        super().__init__(self.canvas, self.iface)
        # self.snapping_utils = QgsSnappingUtils(canvas)
        self.vertices = []
        self.line_band = QgsRubberBand(self.canvas, Qgis.GeometryType.Line)
        self.is_digitizing = False
        self.is_undoing = False

    def activate(self):
        super().activate()
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage("Create Lines:", duration=0)

    def reset(self):
        self.line_band.reset(Qgis.GeometryType.Line)
        super().reset()
        self.iface.messageBar().pushMessage("Create Lines:", duration=0)

    def deactivate(self):
        self.line_band.reset(Qgis.GeometryType.Line)
        super().deactivate()

    def canvasPressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.deactivate()
        elif e.button() == Qt.LeftButton:
            self.line_band.addPoint(e.mapPoint())
            self.vertices.append(e.mapPoint())

    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space]:
            if self.is_undoing == False:
                self.deactivate()
            else:
                self.is_undoing = True
                self.vertices.pop()
                self.line_band.reset()
                for vertex in self.vertices:
                    self.line_band.addPoint(vertex)
        elif e.key() == Qt.Key_U:
            if self.is_undoing == False:
                self.is_undoing = True
            else:
                self.is_undoing = False
        elif e.key() == Qt.Key_Escape:
            self.deactivate()
        else:
            pass
