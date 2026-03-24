from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from ..structure.Question import Question
from .RatingWidget import RatingWidget

class QuestionWidget(QWidget):
    """ A widget representing a question, with the question text and rating """
    def __init__(self, question : Question, parent=None):
        super().__init__(parent)

        self.question = question

        label = QLabel(question.text)
        ratingWidget = RatingWidget(question.rating)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(ratingWidget)

        self.setLayout(layout)
        