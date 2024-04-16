from qgis.core import QgsApplication
import os
from qgis.utils import iface
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .options import CivilToolsOptionsFactory

app = QgsApplication.instance()
plugin_path = app.qgisSettingsDirPath()
__main_menu__ = "CivilTools"
__create_menu__ = "Create Geometry"
__modify_menu__ = "Modify Geometry"
__civil_menu__ = "Create Civil Data"
__analyze_menu__ = "Analyze"
__survey_menu__ = "Survey Tools"
line_icon = QIcon(':/images/themes/default/mIconLineLayer.svg')
arc_icon = QIcon(':/images/themes/default/mActionDigitizeWithCurve.svg')
circle_icon = QIcon(':/images/themes/default/mActionCircle2Points.svg')
curve_icon = QIcon(':/images/themes/default/labelingCalloutCurved.svg')
point_icon = QIcon(':/images/themes/default/mIconPointLayer.svg')
rectangle_icon = QIcon(':/images/themes/default/mActionRectangleExtent.svg')
ellipse_icon = QIcon(':/images/themes/default/mActionEllipseCenterPoint.svg')
dimension_icon = QIcon(':/images/themes/default/mActionMeasure.svg')

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
        self.lineAction = QAction(line_icon, "Create Lines...")
        self.createMenu.addAction(self.lineAction)
        self.options_factory = CivilToolsOptionsFactory()
        self.options_factory.setTitle('CivilTools')
        iface.registerOptionsWidgetFactory(self.options_factory)

    def unload(self):
        self.iface.pluginMenu().removeAction(self.mainMenu.menuAction())
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)
