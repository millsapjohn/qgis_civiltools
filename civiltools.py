from qgis.core import QgsApplication
import os
from qgis.utils import iface
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .options import CivilToolsOptionsFactory
from .resources.cursor_builder import CTCursor

app = QgsApplication.instance()
plugin_path = app.qgisSettingsDirPath()
__main_menu__ = "CivilTools"
__create_menu__ = "Create Geometry"
__modify_menu__ = "Modify Geometry"
__civil_menu__ = "Create Civil Data"
__analyze_menu__ = "Analyze"
__survey_menu__ = "Survey Tools"
__dim_menu__ = "Dimensioning Tools"
line_icon = QIcon(":/images/themes/default/mIconLineLayer.svg")
arc_icon = QIcon(":/images/themes/default/mActionDigitizeWithCurve.svg")
circle_icon = QIcon(":/images/themes/default/mActionCircle2Points.svg")
curve_icon = QIcon(":/images/themes/default/labelingCalloutCurved.svg")
point_icon = QIcon(":/images/themes/default/mIconPointLayer.svg")
rectangle_icon = QIcon(":/images/themes/default/mActionRectangleExtent.svg")
ellipse_icon = QIcon(":/images/themes/default/mActionEllipseCenterPoint.svg")
dimension_icon = QIcon(":/images/themes/default/mActionMeasure.svg")
polygon_icon = QIcon(":/images/themes/default/mActionAddPolygon.svg")
polyline_icon = QIcon(":/images/themes/default/mLayoutItemPolyline.svg")
placeholder_icon = QIcon(":/qt-project.org/styles/commonstyle/images/titlebar-contexthelp-16.png")


class CivilToolsPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.mainMenu = self.iface.pluginMenu().addMenu(__main_menu__)
        self.createMenu = self.mainMenu.addMenu(__create_menu__)
        self.modifyMenu = self.mainMenu.addMenu(__modify_menu__)
        self.civilMenu = self.mainMenu.addMenu(__civil_menu__)
        self.analyzeMenu = self.mainMenu.addMenu(__analyze_menu__)
        self.surveyMenu = self.mainMenu.addMenu(__survey_menu__)
        self.dimMenu = self.mainMenu.addMenu(__dim_menu__)
        self.initializeAction = QAction("Initialize Project")
        self.mainMenu.addAction(self.initializeAction)
        self.draftingModeAction = QAction("Activate Drafting Mode")
        self.mainMenu.addAction(self.draftingModeAction)
        self.initCreateMenu()
        self.initModifyMenu()
        self.initCivilMenu()
        self.initAnalyzeMenu()
        self.initDimMenu()
        self.options_factory = CivilToolsOptionsFactory()
        self.options_factory.setTitle("CivilTools")
        self.iface.registerOptionsWidgetFactory(self.options_factory)

    def unload(self):
        self.iface.pluginMenu().removeAction(self.createMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.modifyMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.civilMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.analyzeMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.surveyMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.dimMenu.menuAction())
        self.iface.pluginMenu().removeAction(self.mainMenu.menuAction())
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)

    def initCreateMenu(self):
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
        self.squareAction = QAction(placeholder_icon, "Create Squares...")
        self.createMenu.addAction(self.squareAction)

    def initModifyMenu(self):
        self.trimAction = QAction(placeholder_icon, "Trim...")
        self.modifyMenu.addAction(self.trimAction)
        self.extendAction = QAction(placeholder_icon, "Extend...")
        self.modifyMenu.addAction(self.extendAction)
        self.lengthenAction = QAction(placeholder_icon, "Lengthen...")
        self.modifyMenu.addAction(self.lengthenAction)
        self.scaleAction = QAction(placeholder_icon, "Scale...")
        self.modifyMenu.addAction(self.scaleAction)
        self.rotateAction = QAction(placeholder_icon, "Rotate...")
        self.modifyMenu.addAction(self.rotateAction)
        self.offsetAction = QAction(placeholder_icon, "Offset...")
        self.modifyMenu.addAction(self.offsetAction)
        self.mirrorAction = QAction(placeholder_icon, "Mirror...")
        self.modifyMenu.addAction(self.mirrorAction)
        self.alignAction = QAction(placeholder_icon, "Align...")
        self.modifyMenu.addAction(self.alignAction)
        self.stretchAction = QAction(placeholder_icon, "Stretch...")
        self.modifyMenu.addAction(self.stretchAction)
        self.filletAction = QAction(placeholder_icon, "Fillet...")
        self.modifyMenu.addAction(self.filletAction)
        self.chamferAction = QAction(placeholder_icon, "Chamfer...")
        self.modifyMenu.addAction(self.chamferAction)
        self.breakPointAction = QAction(placeholder_icon, "Break at Point...")
        self.modifyMenu.addAction(self.breakPointAction)
        self.breakAction = QAction(placeholder_icon, "Break Between Points...")
        self.modifyMenu.addAction(self.breakAction)
        self.peditAction = QAction(placeholder_icon, "Edit Polylines...")
        self.modifyMenu.addAction(self.peditAction)
        self.arrayAction = QAction(placeholder_icon, "Array...")
        self.modifyMenu.addAction(self.arrayAction)

    def initCivilMenu(self):
        pass

    def initAnalyzeMenu(self):
        pass

    def initDimMenu(self):
        pass
