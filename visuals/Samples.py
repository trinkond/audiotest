# Written by Ondrej Trinkewitz
# Holds the object widgets for the visual user interface

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt6.QtWidgets import QStyle
from PyQt6.QtCore import Qt, QSize, pyqtSignal

from ..Samples import Sample
from ..Questions import Question, RatingDiscrete, RatingContinuous, Rating

class SampleWidget(QWidget):
    def __init__(self, sample : Sample):
        super().__init__()

        self.sample = sample   # store reference to the sample object

        label = QLabel(sample.id)
        play_button = QPushButton("Play")

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(play_button)

        self.setLayout(layout)


class QuestionWidget(QWidget):
    def __init__(self, question : Question):
        super.__init__()

        self.question = question

        label = QLabel(question.id)
        