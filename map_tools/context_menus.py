from qgis.PyQt.QtWidgets import QMenu, QAction

def baseContextMenu(menu: QMenu):
    coord_separator = menu.addSeparator()
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

    calc_action = menu.addAction("Launch Calculator")
    select_action = menu.addAction("Select...")
    find_action = menu.addAction("Find...")
    options_action = menu.addAction("Options...")
    misc_separator = menu.addSeparator()

def selectedContextMenu(menu: QMenu):
    prop_action = menu.addAction("Properties")
    similar_action = menu.addAction("Select Similar")
    count_action = menu.addAction("Count Selected")
    selected_separator = menu.addSeparator()

def lineContextMenu(menu: QMenu):
    prof_action = menu.addAction("Quick Profile")
    pline_action = menu.addAction("Convert to Polyline")
    line_separator = menu.addSeparator()

def plineContextMenu(menu: QMenu):
    prof_action = menu.addAction("Quick Profile")
    pedit_action = menu.addAction("Polyline Edit")
    close_action = menu.addAction("Close Polyline")
    pline_separator = menu.addSeparator()

def alignContextMenu(menu: QMenu):
    align_menu = menu.addMenu("Edit Alignment")
    surfprof_action = align_menu.addAction("Create Profile from Surface")
    drawprof_action = align_menu.addAction("Create Profile by Layout")
    offset_action = align_menu.addAction("Create Offset Alignment")
    align_separator = menu.addSeparator()

def surfContextMenu(menu: QMenu):
    surf_menu = menu.addMenu("Edit Surface")
    surfed_action = surf_menu.addAction("Launch Surface Editor")
    points_action = surf_menu.addAction("Edit Points")
    edges_action = surf_menu.addAction("Edit TIN Triangles")
    surf_separator = menu.addSeparator()

def blineContextMenu(menu: QMenu):
    bl_menu = menu.addMenu("Edit Breakline")
    bleditor_action = bl_menu.addAction("Launch Breakline Editor")
    rl_action = bl_menu.addAction("Raise/Lower Breakline")
    drape_action = bl_menu.addAction("Drape Breakline on Surface")
    tosurf_action = bl_menu.addAction("Add Breakline to Surface")
    bl_separator = menu.addSeparator()

def regionContextMenu(menu: QMenu):
    region_menu = menu.addMenu("Edit Grading Region")
    reged_action = region_menu.addAction("Launch Region Editor")
    al_action = region_menu.addAction("Add Alignment to Region")
    subr_action = region_menu.addAction("Add Subregion")
    join_action = region_menu.addAction("Join Subregions")
    subpr_action = region_menu.addAction("Edit Subregion Properties")
    region_separator = menu.addSeparator()

def networkContextMenu(menu: QMenu):
    net_menu = menu.addMenu("Edit Pipe Network")
    netedit_action = net_menu.addAction("Launch Pipe Network Editor")
    partedit_action = net_menu.addAction("Edit Part Properties")
    swap_action = net_menu.addAction("Swap Part")
    net_separator = menu.addSeparator()
