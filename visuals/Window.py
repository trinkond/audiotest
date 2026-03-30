
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PyQt6.QtCore import Qt
from ..structure.Test import Test
from .TestWidget import TestWidget

class Window(QWidget):
    """ The main window of the test app allowing for scrolling """

    def __init__(self, test : Test, parent=None):
        super().__init__(parent)

        self.test = test
        testWidget = TestWidget(test)

        scrollWidget = QScrollArea()
        scrollWidget.setWidget(testWidget)
        scrollWidget.setWidgetResizable(True)
        scrollWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("My awesome testing app"))
        layout.addWidget(scrollWidget)

        self.setLayout(layout)
