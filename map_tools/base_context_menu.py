from qgis.PyQt.QtWidgets import QMenu, QAction

def baseContextMenu():
    base_context_menu = QMenu()
    snaps_action = QAction("Snaps")
    base_context_menu.addAction(snaps_action)
    return base_context_menu
