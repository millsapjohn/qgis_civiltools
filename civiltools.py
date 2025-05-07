from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsExpressionContextUtils,
    QgsProviderRegistry,
    QgsVectorLayer,
)
import os
from osgeo import ogr
from qgis.utils import iface
from qgis.PyQt.QtWidgets import QAction
from .settings_tools.options import CivilToolsOptionsFactory
from .resources.icons import *
from .map_tools.base_map_tool import BaseMapTool
from qgis.gui import QgsMapToolPan
from .settings_tools.init_error_dialog import initErrorDialog
from .settings_tools.init_dialog import initDialog
from .settings_tools.gpkg_builder import gpkgBuilder

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
        self.initializeAction = QAction(settings_icon, "Initialize Project")
        self.mainMenu.addAction(self.initializeAction)
        self.initializeAction.triggered.connect(self.initializeProject)
        self.draftingModeAction = QAction(
            cad_icon, "Toggle Drafting Mode", self.iface.mainWindow()
        )
        # register a keyboard shortcut to launch drafting mode
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

    def initToolbar(self):
        pass

    def draftingMapTool(self):
        project = QgsProject.instance()
        # check if project has been initialized before launching drafting mode
        if not QgsExpressionContextUtils.projectScope(project).variable("CAD_file"):
            iface.messageBar().pushMessage("Project has not been initialized")
        elif isinstance(self.iface.mapCanvas().mapTool(), BaseMapTool):
            # remove base message
            self.iface.messageBar().clearWidgets()
            # reset default Pan tool
            self.panTool = QgsMapToolPan(self.iface.mapCanvas())
            self.iface.mapCanvas().setMapTool(self.panTool)
            self.iface.messageBar().pushMessage("Drafting Mode Deactivated")
        else:
            self.mapTool = BaseMapTool(self.iface.mapCanvas(), self.iface)
            self.iface.mapCanvas().setMapTool(self.mapTool)
            self.iface.messageBar().pushMessage("Drafting Mode", duration=0)

    def initializeProject(self):
        project = QgsProject.instance()
        # CivilTools only works with projected coordinate systems
        if project.crs().isGeographic() == True:
            dialog = initErrorDialog()
            dialog.exec()
        elif QgsExpressionContextUtils.projectScope(project).variable("initialized"):
            iface.messageBar().pushMessage("Project Has Already Been Initialized")
        else:
            dialog = initDialog()
            dialog.exec()
            if dialog.success == True:
                if not hasattr(dialog, "filename"):
                    iface.messageBar().pushMessage("No filename specified")
                else:
                    self.filename = dialog.filename
                    self.createPackage()

    def createPackage(self):
        # create default CAD layers GeoPackage
        project = QgsProject.instance()
        md = QgsProviderRegistry.instance().providerMetadata("ogr")
        if self.filename:
            QgsExpressionContextUtils.setProjectVariable(
                project, "CAD_file", self.filename
            )
            basename = os.path.basename(self.filename)
            gpkgBuilder(self.filename)
            layers = [l.GetName() for l in ogr.Open(self.filename)]
            first_layer = layers[0]
            layer_path = self.filename + "|layername={first_layer}"
            vl = QgsVectorLayer(layer_path, basename, "ogr")
            conn = md.createConnection(vl.dataProvider().dataSourceUri(), {})
            md.saveConnection(conn, basename)
            iface.reloadConnections()
            # add all CAD layers to a dedicated group
            group_name = "CAD Layers"
            root = project.layerTreeRoot()
            group = root.addGroup(group_name)
            for layer in layers:
                layer_path = self.filename + f"|layername={layer}"
                vl = QgsVectorLayer(layer_path, layer, "ogr")
                project.addMapLayer(vl)
                if not vl.isEditable():
                    vl.startEditing()
                vlid = root.findLayer(vl.id())
                # adding a clone and deleting the original seems to be
                # the best way to move between groups
                clone = vlid.clone()
                group.insertChildNode(0, clone)
                vlid.parent().removeChildNode(vlid)
                # collapse group by default to avoid cluttering the layer tree
                group.setExpanded(False)
            # works in concert with the Project Setup plugin, if it's been installed, 
            # to manage persistent connections
            if QgsExpressionContextUtils.projectScope(project).variable(
                "project_gpkg_connections"
            ):
                connections = QgsExpressionContextUtils.projectScope(project).variable(
                    "project_gpkg_connections"
                )
                connections = connections + basename + ";" + self.filename + ";"
                QgsExpressionContextUtils.setProjectVariable(
                    project, "project_gpkg_connections", connections
                )
            else:
                connections = basename + ";" + self.filename + ";"
                QgsExpressionContextUtils.setProjectVariable(
                    project, "gpkg_connections", connections
                )
