
from PyQt6.QtCore import QObject, pyqtSignal
from ..visuals.SampleWidget import SampleWidget
from ..Player import Player

class PlaybackControl(QObject):

    def __init__(self, player : Player):
        super().__init__()
        self.player = player
        self.currentSample = None

        player.finished.connect(self.playbackStop)

    def registerSample(self, sample : SampleWidget):
        sample.requestPlayback.connect(self.playbackStart)
        sample.requestStop.connect(self.playbackStop)

    def registerSamplesRecursive(self, obj : QObject):
        """ Connects all sample widgets in the object tree """
        if isinstance(obj, SampleWidget):
            self.registerSample(obj)
        for child in obj.findChildren(QObject):
            self.registerSamplesRecursive(child)

    def playbackStart(self, widget : SampleWidget):
        sample = widget.sample
        if not self.player.playing():           # if the player is free, start playback
            self.player.playSample(sample)
            widget.setPlaying()
            self.currentSample = widget

    def playbackStop(self):
        self.player.stop()
        if self.currentSample is not None:
            self.currentSample.setStopped()
        self.currentSample = None


