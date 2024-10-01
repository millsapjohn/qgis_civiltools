# QGIS CivilTools

CAD commands for QGIS.

## Basic Concepts

CivilTools aims to provide a CAD-like drawing experience in QGIS - keyboard shortcuts for commands, common geometry creation and modification tools, and options for creating 3d data like pipe networks or TIN surfaces.

### Default Layers, Initialization

In order to facilitate easy geometry creation, CivilTools uses default geometry layers for the objects you create. In order to use CivilTools, it must be initialized on a per-project basis. This is accomplished by opening the Plugins menu, CivilTools sub-menu, and clicking the "Initialize Project" button. <br>

A popup menu will appear, prompting you to either designate default geometry layers that already exist in the drawing, or to create a new GeoPackage with default layers pre-loaded. Default layers will be specified for the following:

- points
- lines
- polygons
- TIN points
- TIN triangles
- grading points
- grading lines
- corridor lines
- corridor polygons
- pipe network nodes
- pipe network conduits
