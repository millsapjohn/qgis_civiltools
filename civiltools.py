from qgis.core import QgsApplication
import os
from qgis.utils import iface
from qgis.gui import QgsGui
from qgis.PyQt.QtWidgets import QAction
from .options import CivilToolsOptionsFactory
from .resources.cursor_builder import CTCursor
from .resources.icons import *

app = QgsApplication.instance()


class CivilToolsPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.mainMenu = self.iface.pluginMenu().addMenu("CivilTools")
        self.initCreateMenu()
        self.initModifyMenu()
        self.initCivilMenu()
        self.initAnalyzeMenu()
        self.initSurveyMenu()
        self.initDimMenu()
        self.initToolbar()
        self.validateCursor()
        self.initializeAction = QAction(settings_icon, "Initialize Project")
        self.mainMenu.addAction(self.initializeAction)
        self.draftingModeAction = QAction(cad_icon, "Activate Drafting Mode", self.iface.mainWindow())
        self.iface.registerMainWindowAction(self.draftingModeAction, "Ctrl+Return")
        self.draftingModeAction.triggered.connect(self.draftingMapTool)
        self.mainMenu.addAction(self.draftingModeAction)        
        self.initOptions()

    def unload(self):
        self.iface.pluginMenu().removeAction(self.createMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.modifyMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.civilMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.analyzeMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.surveyMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.dimMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.mainMenu.menuAction())
        self.iface.unregisterMainWindowAction(self.draftingModeAction)
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)

    def initCreateMenu(self):
        self.createMenu = self.mainMenu.addMenu("Create Geometry")
        self.pointAction = QAction(point_icon, "Create Points...")
        self.createMenu.addAction(self.pointAction)
        self.lineAction = QAction(line_icon, "Create Lines...")
        self.createMenu.addAction(self.lineAction)
        self.plineAction = QAction(polyline_icon, "Create Polylines...")
        self.createMenu.addAction(self.plineAction)
        self.arcAction = QAction(arc_icon, "Create Arcs...")
        self.createMenu.addAction(self.arcAction)
        self.polygonAction = QAction(polygon_icon, "Create Polygons...")
        self.createMenu.addAction(self.polygonAction)
        self.circleAction = QAction(circle_icon, "Create Circles...")
        self.createMenu.addAction(self.circleAction)
        self.ellipseAction = QAction(ellipse_icon, "Create Ellipses...")
        self.createMenu.addAction(self.ellipseAction)
        self.rectangleAction = QAction(rectangle_icon, "Create Rectangles...")
        self.createMenu.addAction(self.rectangleAction)
        self.squareAction = QAction(square_icon, "Create Squares...")
        self.createMenu.addAction(self.squareAction)

    def initModifyMenu(self):
        self.modifyMenu = self.mainMenu.addMenu("Modify Geometry")
        self.trimAction = QAction(trim_icon, "Trim...")
        self.modifyMenu.addAction(self.trimAction)
        self.extendAction = QAction(trim_icon, "Extend...")
        self.modifyMenu.addAction(self.extendAction)
        self.lengthenAction = QAction(lengthen_icon, "Lengthen...")
        self.modifyMenu.addAction(self.lengthenAction)
        self.scaleAction = QAction(scale_icon, "Scale...")
        self.modifyMenu.addAction(self.scaleAction)
        self.rotateAction = QAction(rotate_icon, "Rotate...")
        self.modifyMenu.addAction(self.rotateAction)
        self.offsetAction = QAction(offset_icon, "Offset...")
        self.modifyMenu.addAction(self.offsetAction)
        self.mirrorAction = QAction(placeholder_icon, "Mirror...")
        self.modifyMenu.addAction(self.mirrorAction)
        self.alignAction = QAction(align_icon, "Align...")
        self.modifyMenu.addAction(self.alignAction)
        self.stretchAction = QAction(stretch_icon, "Stretch...")
        self.modifyMenu.addAction(self.stretchAction)
        self.filletAction = QAction(fillet_icon, "Fillet...")
        self.modifyMenu.addAction(self.filletAction)
        self.chamferAction = QAction(fillet_icon, "Chamfer...")
        self.modifyMenu.addAction(self.chamferAction)
        self.breakPointAction = QAction(break_icon, "Break at Point...")
        self.modifyMenu.addAction(self.breakPointAction)
        self.breakAction = QAction(break_icon, "Break Between Points...")
        self.modifyMenu.addAction(self.breakAction)
        self.peditAction = QAction(pedit_icon, "Edit Polylines...")
        self.modifyMenu.addAction(self.peditAction)
        self.arrayAction = QAction(array_icon, "Array...")
        self.modifyMenu.addAction(self.arrayAction)

    def initCivilMenu(self):
        self.civilMenu = self.mainMenu.addMenu("Create Civil Data")

    def initAnalyzeMenu(self):
        self.analyzeMenu = self.mainMenu.addMenu("Analyze")

    def initSurveyMenu(self):
        self.surveyMenu = self.mainMenu.addMenu("Survey Tools")
        
    def initDimMenu(self):
        self.dimMenu = self.mainMenu.addMenu("Dimensioning Tools")

    def initOptions(self):
        self.options_factory = CivilToolsOptionsFactory()
        self.options_factory.setTitle("CivilTools")
        self.iface.registerOptionsWidgetFactory(self.options_factory)

    def validateCursor(self):
        pluginpath = os.path.dirname(os.path.realpath(__file__))
        extension = os.path.join(pluginpath, 'resources\\cursor.png')
        if os.path.exists(extension):
            pass
        else:
            new_cursor = CTCursor(6, 100, (0,0,0), extension)
            new_cursor.drawCursor()
            
    def initToolbar(self):
        pass

    def draftingMapTool(self):
        self.iface.messageBar().pushMessage("action triggered")
