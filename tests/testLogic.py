""" Testing of the test logic (playback policy and rating lock) """

import logging
logging.basicConfig(level=logging.INFO)

import sys
from PyQt6.QtWidgets import QApplication
from ..logic.RatingLockLogic import RatingLockLogic
from ..logic.PlaybackControl import PlaybackControl
from ..player.Player import Player
from ..structure.Sample import Sample, Region
from ..structure.Question import Question
from ..structure.Rating import RatingContinuous, RatingDiscrete
from ..structure.Playlist import Playlist
from ..structure.Test import Test
from ..visuals.Window import Window

app = QApplication(sys.argv)

reg = Region(0.0, 15.778)
samples = [Sample(2, reg), Sample(3, reg), Sample(4, reg)]
questions = [
    Question("What was the quality?", RatingContinuous(0, 100)),
    Question("How much you like the sample?", RatingDiscrete({1: "Hate it", 2: "It's ok", 3: "Love it"})),
    ]
playlist = Playlist(samples, None, questions)

test = Test([playlist])

window = Window(test)
window.setWindowTitle(test.title)

player = Player(volume=0.5)
player.initReaper()
playback = PlaybackControl(player, window, inOrder=False, allowRepeat=True, allowStop=True)
ratingLock = RatingLockLogic(playback, window, rateAny=False, rateAfter=True)

window.show()

sys.exit(app.exec())
