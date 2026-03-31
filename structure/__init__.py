""" A module containing classes to represent the test structure,
also contains functions to load and save the structure as json """

from .Sample import Sample, Region, read_config
from .Question import Question
from .Rating import Rating, RatingDiscrete, RatingContinuous, Value
from .Playlist import Playlist
from .Test import Test, loadTest


