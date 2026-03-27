from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QStyle
from PyQt6.QtCore import pyqtSignal

from ..structure.Sample import Sample
from ..Player import Player

class SampleWidget(QWidget):
    """ A widget representing a sample that can be played, with a play controls and a label """

    requestPlayback = pyqtSignal(object)
    requestStop = pyqtSignal()

    def __init__(self, sample : Sample, parent=None):
        super().__init__(parent)

        self.sample = sample   # store reference to the sample

        label = QLabel(sample.id)
        self.button = QPushButton()
        self.button.setFixedSize(40, 40)
        self.setStopped()

        layout = QHBoxLayout()
        
        layout.addWidget(self.button)
        layout.addWidget(label)

        self.button.clicked.connect(self.buttonClicked)

        self.setLayout(layout)

    def buttonClicked(self, state):
        if not self.playing:
            self.requestPlayback.emit(self)
        else:
            self.requestStop.emit()

    def setStopped(self):   # show the play icon
        self.playing = False
        self.button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def setPlaying(self):   # show the stopped icon
        self.playing = True
        self.button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop))

