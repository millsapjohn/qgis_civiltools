from enum import Enum


def baseKeyValidator(str):
    raw_match = ""
    matches = []
    # match command shortcut first
    for command in Commands:
        if str == command.value:
            raw_match = command.value
            matches.append([command.value, command.name])
    # if other commands contain the string, add them to list of matches
    for command in Commands:
        if str in command.value and command.value != raw_match:
            matches.append([command.value, command.name])
            continue
        if str in command.name and command.value != raw_match:
            if [command.value, command.name] not in matches:
                matches.append([command.value, command.name])
    if len(matches) == 0:
        result = (False, [])
    elif len(matches) > 4:
        matches = matches[0:4]
        result = (True, matches)
    else:
        result = (True, matches)
    return result


class Commands(Enum):
    ARC = "A"
    CREATE_ALIGNMENT_FROM_OBJECT = "AFO"
    ALIGN = "AL"
    CREATE_OFFSET_ALIGNMENT = "ALO"
    ARRAY = "ARR"
    MEASURE_AREA = "AR"
    EDIT_BREAKLINE = "BED"
    BREAK = "BR"
    BREAKLINE = "BRL"
    BREAK_AT_POINT = "BRP"
    CIRCLE = "C"
    MEASURE_ANGLE = "CGA"
    CHAMFER = "CH"
    CHANGE_LAYER = "CHL"
    CLOSE_POLYLINE = "CLO"
    COPY = "CO"
    ALIGNED_DIMENSION = "DAL"
    ANGULAR_DIMENSION = "DAN"
    ARC_DIMENSION = "DAR"
    CONTINUE_DIMENSION = "DCO"
    DIAMETER_DIMENSION = "DDA"
    MEASURE_DISTANCE = "DI"
    LINEAR_DIMENSION = "DLI"
    RADIUS_DIMENSION = "DRA"
    ERASE = "E"
    ELLIPSE = "EL"
    EXTEND = "EX"
    EXCLUDE_LAYER_SNAP = "EXC"
    FILLET = "F"
    FLATTEN = "FLA"
    GRADING_REGION = "GR"
    GRADING_TEMPLATE = "GTP"
    HIDE_OBJECTS = "HIO"
    ISOLATE_OBJECTS = "ISO"
    JOIN = "J"
    LINE = "L"
    LABEL = "LAB"
    LAYER_FREEZE = "LAF"
    LAYER_THAW = "LAT"
    LINE_CURVE_INFO = "LCP"
    LENGTHEN = "LEN"
    LIST_PROP = "LS"
    MOVE = "M"
    MATCH_PROP = "MA"
    MIRROR = "MI"
    MTEXT = "MT"
    NOTE = "NOT"
    OFFSET = "O"
    ORTHO_MODE = "ORT"
    POLYLINE_EDIT = "PED"
    POLYGON = "PG"
    CREATE_PIPE_NETWORK = "PIN"
    POLYLINE = "PL"
    POINT = "PO"
    OFFSET_PROFILE = "POF"
    PROJECTED_PROFILE = "PPR"
    PROPERTIES = "PR"
    PROFILE_MANAGER = "PRF"
    PROFILE_BY_LAYOUT = "PRL"
    PROFILE_FROM_SURFACE = "PRS"
    SUPERIMPOSED_PROFILE = "PSU"
    REDO = "R"
    REVERSE = "RE"
    RECTANGLE = "REC"
    EDIT_GRADING_REGION = "RED"
    ROTATE = "RO"
    REVCLOUD = "RVC"
    SCALE = "SC"
    SELECT_DISTANCE = "SD"
    SECTION_MANAGER = "SEC"
    PROJECTED_SECTION = "SEP"
    SELECT_FREEHAND = "SF"
    SELECT_LOCATION = "SL"
    SAMPLE_LINES = "SLP"
    SNAP_MANAGER = "SNA"
    SQUARE = "SQ"
    SELECT_RADIUS = "SR"
    STRETCH = "STR"
    SELECT_VALUE = "SV"
    TRIM = "TR"
    UNDO = "U"
    UNISOLATE = "UNI"
    VOLUME_MANAGER = "VOD"
    WIPEOUT = "WIP"
    EXPLODE = "X"
    
