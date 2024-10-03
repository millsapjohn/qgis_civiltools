from qgis.gui import (
    QgsMapCanvas,
    QgsMapMouseEvent,
    QgsRubberBand,
    QgsMapTool,
)

class BaseMapTool(QgsMapTool):
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapTool.__init__(self, self.canvas)

    def reset(self):
        pass

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()
