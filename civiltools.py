from qgis.core import QgsApplication
import os
from qgis.core import iface
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon

app = QgsApplication.instance()
plugin_path = app.qgisSettingsDirPath()
line_icon = 'line.png'
line_icon_path = os.path.join(plugin_path, 'python/plugins/CivilTools/Resources', line_icon)
main_menu = "CivilTools"
line_icon = QIcon(line_icon_path)

class CivilToolsPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.lineAction = QAction(line_icon, "Draw Line")
        self.iface.addPluginToMenu(main_menu, self.lineAction)

    def unload(self):
        self.iface.removePluginMenu(main_menu, self.lineAction)
