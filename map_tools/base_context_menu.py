from qgis.PyQt.QtWidgets import QMenu, QAction

def baseContextMenu(menu: QMenu):
    repeat_action = menu.addAction("Repeat Last Command")
    repeat_separator = menu.addSeparator()

    snaps_menu = menu.addMenu("Snaps")
    toggle_action = snaps_menu.addAction("Toggle Snapping")
    vertex_action = snaps_menu.addAction("Vertex")
    midpoint_action = snaps_menu.addAction("Midpoint")
    center_action = snaps_menu.addAction("Center")
    node_action = snaps_menu.addAction("Node")
    inter_action = snaps_menu.addAction("Intersection")
    perp_action = snaps_menu.addAction("Perpendicular")
    tan_action = snaps_menu.addAction("Tangent")
    near_action = snaps_menu.addAction("Nearest")
    snaps_separator = menu.addSeparator()

    iso_menu = menu.addMenu("Isolate Features...")
    iso_action = iso_menu.addAction("Isolate Feature(s)")
    hide_action = iso_menu.addAction("Hide Feature(s)")
    uniso_action = iso_menu.addAction("Unhide Feature(s)")
    iso_separator = menu.addSeparator()

    clipb_menu = menu.addMenu("Clipboard")
    cut_action = clipb_menu.addAction("Cut Feature(s)")
    copy_action = clipb_menu.addAction("Copy Feature(s)")
    paste_action = clipb_menu.addAction("Paste Feature(s)")
    clipb_separator = menu.addSeparator()

    select_action = menu.addAction("Select...")
    find_action = menu.addAction("Find...")
    options_action = menu.addAction("Options...")
