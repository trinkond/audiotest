from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal

from ..structure.Sample import Sample

class SampleWidget(QWidget):
    """ A widget representing a sample that can be played, with a play controls and a label """

    startPlayback = pyqtSignal(object)  # emits the sample object when play button is clicked
    stopPlayback = pyqtSignal()         # sends a command to force stop the playback

    def __init__(self, sample : Sample, parent=None):
        super().__init__(parent)

        self.sample = sample   # store reference to the sample object

        label = QLabel(sample.id)
        play_button = QPushButton("Play")

        layout = QHBoxLayout()
        
        layout.addWidget(play_button)
        layout.addWidget(label)

        self.setLayout(layout)
