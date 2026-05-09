""" Testing of the application as a whole (AppMain) """

import logging
logging.basicConfig(level=logging.INFO)

import sys

from ..structure.Sample import Sample, Region
from ..structure.Question import Question
from ..structure.Rating import RatingContinuous, RatingDiscrete
from ..structure.Playlist import Playlist
from ..structure.Test import Test
from ..structure.Settings import Settings

from ..logic.AppMain import AppMain

""" Some sample test """
reg = Region(0.0, 15.778)
samples = [Sample(2, reg), Sample(3, reg), Sample(4, reg)]
questions = [
    Question("What was the quality?", RatingContinuous(0, 100)),
    Question("How much you like the sample?", RatingDiscrete({1: "Hate it", 2: "It's ok", 3: "Love it"})),
    ]
playlist = Playlist(samples, None, questions)
test = Test([playlist], Settings({"require fill previous" : True}))

app = AppMain(test)
ret = app.run()

sys.exit(ret)

