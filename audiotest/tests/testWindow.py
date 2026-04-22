""" Testing the visuals of my PlayList """

import logging
logging.basicConfig(level=logging.INFO)

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from ..structure.Playlist import Playlist
from ..structure.Sample import Sample
from ..structure.Question import Question
from ..structure.Rating import RatingDiscrete, RatingContinuous, Rating
from ..structure.Test import Test
from ..structure.Settings import Settings
from ..visuals.Window import Window
from ..visuals.TestWidget import TestWidget
from ..themes.themes import ThemeList

app = QApplication(sys.argv)

instructions = "Do something productive to test this thing!"
samples = [Sample(1, None, "s1"), Sample(2, None), Sample(3, None)]
questions = [
    Question("What was the quality?", RatingContinuous(0, 100)),
    Question("How much you like the sample?", RatingDiscrete({1: "Hate it", 2: "It's ok", 3: "Love it"})),
    ]
playlist = Playlist(samples, instructions, questions)
sampleless = Playlist([], instructions, questions,name="Sampleless")

test = Test([playlist, sampleless], settings=Settings({"show sample names" : True}))

testWidget = TestWidget(test)
window = Window(testWidget, title="Window test", theme=ThemeList["big"])

window.show()

sys.exit(app.exec())
