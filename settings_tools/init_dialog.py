from PyQt5.QtWidgets import (
    QDialog,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QLineEdit,
)
from qgis.utils import iface
import os


class initDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.iface = iface
        self.success = False
        self.homePath = os.path.expanduser("~")
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Set CAD GeoPackage Location")
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.locationText = QLabel("Set CAD GeoPackage Save Location:")
        self.mainLayout.addWidget(self.locationText)
        self.fileLayout = QHBoxLayout()
        self.fileBox = QLineEdit("Save File Location: ")
        self.fileLayout.addWidget(self.fileBox)
        self.fileButton = QPushButton(text="...")
        self.fileButton.clicked.connect(self.getSaveFile)
        self.fileLayout.addWidget(self.fileButton)
        self.mainLayout.addLayout(self.fileLayout)

        self.submitLayout = QHBoxLayout()
        self.submitButton = QPushButton("Ok")
        self.submitButton.clicked.connect(self.submitValues)
        self.submitLayout.addWidget(self.submitButton)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)
        self.submitLayout.addWidget(self.cancelButton)
        self.mainLayout.addLayout(self.submitLayout)

        # TODO: add level management template selection

    def getSaveFile(self):
        self.filenameDialog = QFileDialog()
        self.filename = self.filenameDialog.getSaveFileName(
            self, "Specify Save Location:", self.homePath, "GeoPackage (*.gpkg)"
        )[0]
        self.fileBox.setText(self.filename)

    def submitValues(self):
        self.success = True
        self.close()
