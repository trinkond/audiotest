""" Testing of the ResultCollector and ItemWidget communication """

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

from ..structure.Sample import Sample
from ..structure.Rating import Rating, RatingContinuous, RatingDiscrete
from ..structure.Question import Question
from ..structure.Playlist import Playlist
from ..visuals.PlaylistWidget import PlaylistWidget
from ..logic.ResultCollector import ResultCollector


rescol = ResultCollector()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Result collection test")

layout = QVBoxLayout()

samples = [
    Sample(1, None),
    Sample(2, None),
    Sample(3, None)
]

rat1 = RatingDiscrete({1 : "Bad", 2 : "Ok", 3 : "Good"})
rat2 = RatingContinuous(1, 10)

quests = [
    Question("What was the quality?", rat2),
    Question("How did you like the song?", rat1),
    Question("Was the volume ok?", rat1)
]

playlist = Playlist(samples, "Listen to the sample and answer all the questions", quests)

layout.addWidget(PlaylistWidget(playlist))

window.setLayout(layout)

# connect all the sample signals to the result collector
rescol.registerItemsRecursive(window)

with open("audiotest/visuals/style.qss", "r") as f:
    app.setStyleSheet(f.read())

window.show()

sys.exit(app.exec())
