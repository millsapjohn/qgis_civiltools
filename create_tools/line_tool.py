from qgis.core import (
    QgsSnappingUtils,
    QgsPointLocator,
    Qgis,
)
from qgis.gui import QgsRubberBand
from qgis.PyQt.QtCore import Qt
from ..map_tools.base_map_tool import BaseMapTool


class LineMapTool(BaseMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        super().__init__(self.canvas, self.iface)
        self.snapping_utils = QgsSnappingUtils(canvas)
        self.vertices = []

    def activate(self):
        self.line_band = QgsRubberBand(self.canvas, Qgis.GeometryType.Line)
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage("Create Lines:", duration=0)

    def reset(self):
        self.line_band.reset(Qgis.GeometryType.Line)
        super.reset()
        self.iface.messageBar().pushMessage("Create Lines:", duration=0)

    def deactivate(self):
        self.line_band.reset(Qgis.GeometryType.Line)
        super.deactivate()

    def canvasPressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.deactivate()
        elif e.button() == Qt.LeftButton:
            pass

    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_Return, Qt.Key_Enter, Qt.Key_Escape, Qt.Key_Space]:
            self.deactivate()
        elif e.key() == Qt.Key_U:
            self.vertices.pop()
        else:
            pass
