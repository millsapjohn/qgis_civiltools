from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout
from qgis.utils import iface


class initErrorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.iface = iface
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Error: Geographic CRS")
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.warningText = QLabel(
            "Error: CivilTools requires that the project be set to a projected coordinate system. Please change the project CRS before continuing."
        )
        self.mainLayout.addWidget(self.warningText)
        self.okButton = QPushButton(text="OK")
        self.okButton.clicked.connect(self.closeDialog)
        self.mainLayout.addWidget(self.okButton)

    def closeDialog(self):
        self.close()
