""" Testing the visuals of my PlayList """

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from ..structure.Playlist import Playlist
from ..structure.Sample import Sample
from ..structure.Question import Question
from ..structure.Rating import RatingDiscrete, RatingContinuous, Rating
from ..visuals.PlaylistWidget import PlaylistWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Rating test")

layout = QVBoxLayout()

instructions = "Do something productive to test this thing!"
samples = [Sample(1, None), Sample(2, None), Sample(3, None)]
questions = [
    Question("What was the quality?", RatingContinuous(0, 100)),
    Question("How much you like the sample?", RatingDiscrete({1: "Hate it", 2: "It's ok", 3: "Love it"})),
    ]
playlist = Playlist(samples, instructions, questions)

layout.addWidget(PlaylistWidget(playlist))

window.setLayout(layout)

# Load the QSS stylessheet
with open("audiotest/visuals/style.qss", "r") as f:
    app.setStyleSheet(f.read())


window.show()

sys.exit(app.exec())
