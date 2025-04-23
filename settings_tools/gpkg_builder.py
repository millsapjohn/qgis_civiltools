from qgis.core import Qgis, QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsField
from PyQt5.QtCore import QVariant
from qgis.utils import iface

def gpkgBuilder(gpkg_path):
    crs = QgsProject.instance().crs()
    uri = gpkg_path
    layers = [
        QgsVectorLayer("LineString", "cad_lines", "memory"),
        QgsVectorLayer("Polygon", "cad_polygons", "memory"),
        QgsVectorLayer("PointZ", "cad_tin_points", "memory"),
        QgsVectorLayer("PolygonZ", "cad_tin_triangles", "memory"),
        QgsVectorLayer("PointZ", "cad_grading_points", "memory"),
        QgsVectorLayer("LineStringZ", "cad_grading_breaklines", "memory"),
        QgsVectorLayer("PolygonZ", "cad_grading_polygons", "memory"),
        QgsVectorLayer("LineStringZ", "cad_grading_region_lines", "memory"),
        QgsVectorLayer("PolygonZ", "cad_grading_region_polygons", "memory"),
        QgsVectorLayer("LineString", "cad_pipes", "memory"),
        QgsVectorLayer("Point", "cad_structures", "memory"),
        QgsVectorLayer("Point", "cad_dimension_points", "memory"),
        QgsVectorLayer("LineString", "cad_dimension_lines", "memory"),
    ]

    layer = QgsVectorLayer("Point", "points", "memory")
    layer.setCrs(crs)
    provider = layer.dataProvider()
    provider.addAttributes([QgsField("level", QVariant.String)])
    layer.updateFields()
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.layerName = layer.name()
    context = QgsProject.instance().transformContext()
    QgsVectorFileWriter.writeAsVectorFormatV2(layer, uri, context, options)
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

    for layer in layers:
        options.layerName = layer.name()
        layer.setCrs(crs)
        provider = layer.dataProvider()
        provider.addAttributes([QgsField("level", QVariant.String)])
        layer.updateFields()
        QgsVectorFileWriter.writeAsVectorFormatV2(layer, uri, context, options)
