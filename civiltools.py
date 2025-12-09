from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsExpressionContextUtils,
    QgsProviderRegistry,
    QgsMapLayer,
    QgsVectorLayer,
)
import os
from osgeo import ogr
from qgis.utils import iface
try:
    from qgis.PyQt.QtWidgets import QAction
except ImportError:
    from qgis.PyQt.QtGui import QAction
from .settings_tools.options import CivilToolsOptionsFactory
from .resources.icons import *
from .map_tools.base_map_tool import BaseMapTool
from .map_tools.select_tool import SelectMapTool
from .create_tools.line_tool import LineMapTool
from qgis.gui import QgsMapToolPan
from .settings_tools.init_error_dialog import initErrorDialog
from .settings_tools.init_dialog import initDialog
from .settings_tools.gpkg_builder import gpkgBuilder


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
        self.draftingModeAction.triggered.connect(self.setSelectTool)
        self.mainMenu.addAction(self.draftingModeAction)
        self.initOptions()
        self.initMapTools()

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
        self.unloadMapTools()

    def initCreateMenu(self):
        self.createMenu = self.mainMenu.addMenu("Create Geometry")
        self.pointAction = QAction(point_icon, "Create Points...")
        self.pointAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.pointTool))
        self.createMenu.addAction(self.pointAction)
        self.lineAction = QAction(line_icon, "Create Lines...")
        self.lineAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.lineTool))
        self.createMenu.addAction(self.lineAction)
        self.plineAction = QAction(polyline_icon, "Create Polylines...")
        self.plineAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.polylineTool))
        self.createMenu.addAction(self.plineAction)
        self.arcAction = QAction(arc_icon, "Create Arcs...")
        self.arcAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.arcTool))
        self.createMenu.addAction(self.arcAction)
        self.polygonAction = QAction(polygon_icon, "Create Polygons...")
        self.polygonAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.polygonTool))
        self.createMenu.addAction(self.polygonAction)
        self.circleAction = QAction(circle_icon, "Create Circles...")
        self.circleAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.polygonTool))
        self.createMenu.addAction(self.circleAction)
        self.ellipseAction = QAction(ellipse_icon, "Create Ellipses...")
        self.ellipseAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.ellipseTool))
        self.createMenu.addAction(self.ellipseAction)
        self.rectangleAction = QAction(rectangle_icon, "Create Rectangles...")
        self.rectangleAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.rectTool))
        self.createMenu.addAction(self.rectangleAction)
        self.squareAction = QAction(square_icon, "Create Squares...")
        self.squareAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.squareTool))
        self.createMenu.addAction(self.squareAction)

    def initModifyMenu(self):
        self.modifyMenu = self.mainMenu.addMenu("Modify Geometry")
        self.trimAction = QAction(trim_icon, "Trim...")
        self.trimAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.trimTool))
        self.modifyMenu.addAction(self.trimAction)
        self.extendAction = QAction(trim_icon, "Extend...")
        self.extendAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.extendTool))
        self.modifyMenu.addAction(self.extendAction)
        self.lengthenAction = QAction(lengthen_icon, "Lengthen...")
        self.lengthenAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.extendTool))
        self.modifyMenu.addAction(self.lengthenAction)
        self.scaleAction = QAction(scale_icon, "Scale...")
        self.scaleAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.scaleTool))
        self.modifyMenu.addAction(self.scaleAction)
        self.rotateAction = QAction(rotate_icon, "Rotate...")
        self.rotateAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.rotateTool))
        self.modifyMenu.addAction(self.rotateAction)
        self.offsetAction = QAction(offset_icon, "Offset...")
        self.offsetAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.offsetTool))
        self.modifyMenu.addAction(self.offsetAction)
        self.mirrorAction = QAction(placeholder_icon, "Mirror...")
        self.mirrorAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.mirrorTool))
        self.modifyMenu.addAction(self.mirrorAction)
        self.alignAction = QAction(align_icon, "Align...")
        self.alignAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.alignTool))
        self.modifyMenu.addAction(self.alignAction)
        self.stretchAction = QAction(stretch_icon, "Stretch...")
        self.stretchAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.stretchTool))
        self.modifyMenu.addAction(self.stretchAction)
        self.filletAction = QAction(fillet_icon, "Fillet...")
        self.filletAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.filletTool))
        self.modifyMenu.addAction(self.filletAction)
        self.chamferAction = QAction(fillet_icon, "Chamfer...")
        self.chamferAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.chamferTool))
        self.modifyMenu.addAction(self.chamferAction)
        self.breakPointAction = QAction(break_icon, "Break at Point...")
        self.breakPointAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.breakAtPointTool))
        self.modifyMenu.addAction(self.breakPointAction)
        self.breakAction = QAction(break_icon, "Break Between Points...")
        self.breakAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.breakTool))
        self.modifyMenu.addAction(self.breakAction)
        self.peditAction = QAction(pedit_icon, "Edit Polylines...")
        self.peditAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.peditTool))
        self.modifyMenu.addAction(self.peditAction)
        self.arrayAction = QAction(array_icon, "Array...")
        self.arrayAction.triggered.connect(lambda: self.iface.mapCanvas().setMapTool(self.arrayTool))
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

    def initMapTools(self):
        self.selectTool = SelectMapTool(self.iface.mapCanvas(), self.iface)
        self.selectTool.toolChangeRequest.connect(self.setOtherTool)
        self.lineTool = LineMapTool(self.iface.mapCanvas(), self.iface)
        self.lineTool.deactivated.connect(self.setSelectTool)

    def unloadMapTools(self):
        self.selectTool = None
        self.lineTool = None

    def checkInitialized(self):
        project = QgsProject.instance()
        if not QgsExpressionContextUtils.projectScope(project).variable('CAD_file'):
            return False
        else:
            return True

    def setSelectTool(self):
        if not self.checkInitialized():
            self.iface.messageBar().pushMessage("Project has not been initialized")
        elif isinstance(self.iface.mapCanvas().mapTool(), BaseMapTool):
            # remove base message
            self.iface.messageBar().clearWidgets()
            # reset default Pan tool
            self.panTool = QgsMapToolPan(self.iface.mapCanvas())
            self.iface.mapCanvas().setMapTool(self.panTool)
            self.iface.messageBar().pushMessage("Drafting Mode Deactivated")
        else:
            self.iface.mapCanvas().setMapTool(self.selectTool)

    def setOtherTool(self, command):
        match command:
            case "A":
                self.iface.mapCanvas().setMapTool(self.arcTool)
            case "AFO":
                self.iface.mapCanvas().setMapTool(self.alignFromObjTool)
            case "AL":
                self.iface.mapCanvas().setMapTool(self.alignTool)
            case "ALO":
                self.iface.mapCanvas().setMapTool(self.alignOffsetTool)
            case "ARR":
                self.iface.mapCanvas().setMapTool(self.arrayTool)
            case "AR":
                self.iface.mapCanvas().setMapTool(self.areaTool)
            case "BED":
                self.iface.mapCanvas().setMapTool(self.breaklineEditTool)
            case "BR":
                self.iface.mapCanvas().setMapTool(self.breakTool)
            case "BRL":
                self.iface.mapCanvas().setMapTool(self.breaklineTool)
            case "BRP":
                self.iface.mapCanvas().setMapTool(self.breakAtPointTool)
            case "C":
                self.iface.mapCanvas().setMapTool(self.circleTool)
            case "CCL":
                self.iface.mapCanvas().setMapTool(self.cpToCADTool)
            case "CGA":
                self.iface.mapCanvas().setMapTool(self.measureAngleTool)
            case "CGL":
                self.iface.mapCanvas().setMapTool(self.cpToGISTool)
            case "CH":
                self.iface.mapCanvas().setMapTool(self.chamferTool)
            case "CHL":
                self.iface.mapCanvas().setMapTool(self.changeLevelTool)
            case "CLO":
                self.iface.mapCanvas().setMapTool(self.closePlineTool)
            case "CO":
                self.iface.mapCanvas().setMapTool(self.cpTool)
            case "DAL":
                self.iface.mapCanvas().setMapTool(self.dimAlignTool)
            case "DAN":
                self.iface.mapCanvas().setMapTool(self.dimAngTool)
            case "DAR":
                self.iface.mapCanvas().setMapTool(self.dimArcTool)
            case "DCO":
                self.iface.mapCanvas().setMapTool(self.dimContTool)
            case "DDA":
                self.iface.mapCanvas().setMapTool(self.dimDiamTool)
            case "DI":
                self.iface.mapCanvas().setMapTool(self.measureDistTool)
            case "DLI":
                self.iface.mapCanvas().setMapTool(self.dimLinearTool)
            case "DRA":
                self.iface.mapCanvas().setMapTool(self.dimRadiusTool)
            case "E":
                self.iface.mapCanvas().setMapTool(self.eraseTool)
            case "EL":
                self.iface.mapCanvas().setMapTool(self.ellipseTool)
            case "EX":
                self.iface.mapCanvas().setMapTool(self.extendTool)
            case "EXC":
                self.iface.mapCanvas().setMapTool(self.excludeLayerTool)
            case "F":
                self.iface.mapCanvas().setMapTool(self.filletTool)
            case "FLA":
                self.iface.mapCanvas().setMapTool(self.flattenTool)
            case "GR":
                self.iface.mapCanvas().setMapTool(self.gradingRegionTool)
            case "GTP":
                pass #TODO: grading region window action
            case "HIO":
                self.iface.mapCanvas().setMapTool(self.hideTool)
            case "ISO":
                self.iface.mapCanvas().setMapTool(self.isolateTool)
            case "J":
                self.iface.mapCanvas().setMapTool(self.joinTool)
            case "L":
                self.iface.mapCanvas().setMapTool(self.lineTool)
            case "LAB":
                self.iface.mapCanvas().setMapTool(self.labelTool)
            case "LAF":
                self.iface.mapCanvas().setMapTool(self.freezeTool)
            case "LAT":
                self.iface.mapCanvas().setMapTool(self.thawTool)
            case "LCP":
                self.iface.mapCanvas().setMapTool(self.lineInfoTool)
            case "LEN":
                self.iface.mapCanvas().setMapTool(self.lengthenTool)
            case "LS":
                self.iface.mapCanvas().setMapTool(self.propertiesTool)
            case "M":
                self.iface.mapCanvas().setMapTool(self.moveTool)
            case "MA":
                self.iface.mapCanvas().setMapTool(self.matchPropTool)
            case "MI":
                self.iface.mapCanvas().setMapTool(self.mirrorTool)
            case "MT":
                self.iface.mapCanvas().setMapTool(self.labelTool)
            case "NOT":
                self.iface.mapCanvas().setMapTool(self.labelTool)
            case "O":
                self.iface.mapCanvas().setMapTool(self.offsetTool)
            case "ORT":
                pass #TODO: ortho mode action
            case "PE":
                self.iface.mapCanvas().setMapTool(self.peditTool)
            case "PED":
                pass #TODO: profile edit window action
            case "PG":
                self.iface.mapCanvas().setMapTool(self.polygonTool)
            case "PIN":
                pass #TODO: pipe network edit window action
            case "PL":
                self.iface.mapCanvas().setMapTool(self.polylineTool)
            case "PO":
                self.iface.mapCanvas().setMapTool(self.pointTool)
            case "POF":
                self.iface.mapCanvas().setMapTool(self.profOffsetTool)
            case "PPR":
                self.iface.mapCanvas().setMapTool(self.profProjectTool)
            case "PR":
                self.iface.mapCanvas().setMapTool(self.propertiesTool)
            case "PRF":
                pass #TODO: profile edit window action
            case "PRL":
                self.iface.mapCanvas().setMapTool(self.profLayoutTool)
            case "PRS":
                self.iface.mapCanvas().setMapTool(self.profSurfTool)
            case "PSU":
                self.iface.mapCanvas().setMapTool(self.profSuperimpTool)
            case "R":
                pass #TODO redo action
            case "RE":
                self.iface.mapCanvas().setMapTool(self.reverseTool)
            case "REC":
                self.iface.mapCanvas().setMapTool(self.rectTool)
            case "RED":
                self.iface.mapCanvas().setMapTool(self.gradRegionEditTool)
            case "RO":
                self.iface.mapCanvas().setMapTool(self.rotateTool)
            case "RVC":
                self.iface.mapCanvas().setMapTool(self.revCloudTool)
            case "SC":
                self.iface.mapCanvas().setMapTool(self.scaleTool)
            case "SD":
                self.iface.mapCanvas().setMapTool(self.selDistTool)
            case "SEC":
                self.iface.mapCanvas().setMapTool(self.sectTool)
            case "SEP":
                self.iface.mapCanvas().setMapTool(self.sectProjTool)
            case "SLP":
                self.iface.mapCanvas().setMapTool(self.sampleLineTool)
            case "SNA":
                pass #TODO snap window
            case "SQ":
                self.iface.mapCanvas().setMapTool(self.squareTool)
            case "SR":
                self.iface.mapCanvas().setMapTool(self.selRadiusTool)
            case "STR":
                self.iface.mapCanvas().setMapTool(self.stretchTool)
            case "SV":
                self.iface.mapCanvas().setMapTool(self.selValTool)
            case "TR":
                self.iface.mapCanvas().setMapTool(self.trimTool)
            case "U":
                pass #TODO undo action
            case "UNI":
                pass #TODO unhide action
            case "VOD":
                pass #TODO volumes dashboard action
            case "WIP":
                self.iface.mapCanvas().setMapTool(self.wipeoutTool)
            case "X":
                self.iface.mapCanvas().setMapTool(self.explodeTool)

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
            root = project.layerTreeRoot()
            for layer in layers:
                layer_path = self.filename + f"|layername={layer}"
                vl = QgsVectorLayer(layer_path, layer, "ogr")
                vl.setFlags(QgsMapLayer.Private)
                project.addMapLayer(vl)
                if not vl.isEditable():
                    vl.startEditing()
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
                    project, "project_gpkg_connections", connections
                )
