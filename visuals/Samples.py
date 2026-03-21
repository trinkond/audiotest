# Written by Ondrej Trinkewitz
# Holds the object widgets for the visual user interface

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt6.QtWidgets import QStyle
from PyQt6.QtCore import Qt, QSize, pyqtSignal

from ..Samples import Sample
from ..Questions import Question, Rating

from .LabeledSlider import LabeledSlider

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

class RatingWidget(QWidget):
    def __init__(self, minimum=0, maximum=100, step = 1):
        super().__init__()

        #self.rating = rating

        layout = QHBoxLayout()

        slider = LabeledSlider(minimum, maximum, step)
        slider.setMaximumWidth(900)  # slider won't grow past 300px

        value_field = QLineEdit()
        value_field.setReadOnly(True)
        value_field.setText(str(slider.value()))
        value_field.setFixedWidth(80)  # fixed width 80px

        slider.valueChanged.connect(lambda v: value_field.setText(str(v)))

        layout.addWidget(slider)
        layout.addWidget(value_field)

        self.setLayout(layout)



class QuestionWidget(QWidget):
    def __init__(self, question : Question):
        super.__init__()

        self.question = question

        label = QLabel(question.id)
        