from .base_map_tool import BaseMapTool
from qgis.gui import QgsRubberBand


class LineMapTool(BaseMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        self.draw_band = QgsRubberBand(self.canvas)
        super.__init__(self, self.canvas, self.iface)
