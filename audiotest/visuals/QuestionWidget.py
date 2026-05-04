from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal
from ..structure.Rating import Value

from ..structure.Question import Question
from .RatingWidget import RatingWidget

class QuestionWidget(QWidget):
    # emit the rating change to for result collection
    ratingChanged = pyqtSignal(Value, tuple)            # value, ( itemID, questionID )

    """ A widget representing a question, with the question text and rating """
    def __init__(self, question : Question, id : int = 0, contextId : int = 0, parent=None):
        super().__init__(parent)

        self.question = question
        self.id = id
        self.contextId = contextId

        label = QLabel(question.text)
        self.ratingWidget = RatingWidget(question.rating)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.ratingWidget)

        self.ratingWidget.ratingChanged.connect(lambda val: self.ratingChanged.emit(val, (self.contextId, self.id)))

        self.setLayout(layout)

    def lockRating(self):
        self.ratingWidget.lock()

    def unlockRating(self):
        self.ratingWidget.unlock()
        