""" Testing of the ResultCollector and ItemWidget communication """

import logging
logging.basicConfig(level=logging.INFO)

import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

from ..structure.Sample import Sample
from ..structure.Rating import Rating, RatingContinuous, RatingDiscrete
from ..structure.Question import Question
from ..structure.Playlist import Playlist
from ..structure.Test import Test
from ..visuals.ItemWidget import ItemWidget
from ..visuals.TestWidget import TestWidget
from ..logic.ResultCollector import ResultCollector

filename = "audiotest/tests/test_results.csv"

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Result collection test")

layout = QVBoxLayout()

samples = [
    Sample(1, None, "My favorite song"),
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

playlist = Playlist(samples, "Listen to the sample and answer all the questions", quests, name="God playlist")
test = Test([playlist])

rescol = ResultCollector(test, metadata="Test,User")

layout.addWidget(TestWidget(test))

window.setLayout(layout)

# connect all the sample signals to the result collector
rescol.registerItemsRecursive(window)

window.show()

ret = app.exec()

if ret == 0:
    try:
        os.remove(filename)         # delete the file to test header writing
    except FileNotFoundError:
        pass
    rescol.saveResults(filename)    # save the results for the first time
    rescol.saveResults(filename)    # save the results again to test appending to an existing file

sys.exit(ret)
