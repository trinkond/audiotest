
import logging
logger = logging.getLogger(__name__)

from PyQt6.QtCore import QObject, pyqtSignal
from ..visuals.SampleWidget import SampleWidget
from ..structure.Sample import Sample
from ..player.Player import Player

class Checklist:
    def __init__(self):
        self.items = []

    def check(self, item):
        if item < 0:
            logger.error(f"Trying to check negative item {item}")
            return
        try:
            self.items[item] = True
        except IndexError:
            self.items.extend([False] * (item + 1 - len(self.items)))
            self.items[item] = True
    
    def isChecked(self, item):
        try:
            return self.items[item]
        except IndexError:
            return False

class PlaybackControl(QObject):
    """ Class holding the playback logic
    Connects to SampleWidget signals and runs the samples using the Player """

    def __init__(self, player : Player, inOrder = False, allowRepeat = True, allowStop = True, parent=None):
        super().__init__(parent)
        self.player = player
        self.playingWidget = None
        self.inOrder = inOrder
        self.allowRepeat = allowRepeat
        self.allowStop = allowStop

        self.itemPlayed = Checklist()   # Holds if an item has been played for repeat checks
        self.lastPlayed = -1            # Holds the last played item for in order playback

        player.finished.connect(self.playbackStop)
        logger.info(f'initialized PlaybackControl with {"in order playback" if inOrder else "free playback"} and repeat {"allowed" if allowRepeat else "not allowed"}') 

    def registerSample(self, sample : SampleWidget):
        sample.requestPlayback.connect(self.playbackStart)
        sample.requestStop.connect(self.playbackStop)

    def registerSamplesRecursive(self, obj : QObject):
        """ Connects all sample widgets in the object tree """
        if isinstance(obj, SampleWidget):
            self.registerSample(obj)
        for child in obj.findChildren(QObject):
            self.registerSamplesRecursive(child)

    def playbackStart(self, sample : Sample, id : int):
        if self.player.playing():               # player busy
            logger.info("Playback requested while player is still playing, ignoring")
            return
        if not self.allowRepeat and self.itemPlayed.isChecked(id):
            logger.info(f"Playback of item {id} requested, but repeats are not allowed, ignoring")
            return
        if self.inOrder and id not in [self.lastPlayed, self.lastPlayed + 1]:
            logger.info(f"Playback of item {id} requested, but only in order playback is allowed and previous item was {self.lastPlayed}, ignoring")
            return

        if self.player.playSample(sample):      # start the playback
            self.playingWidget = self.sender()
            self.playingWidget.setPlaying()     # notify the widget, that the playback has started
            self.itemPlayed.check(id)           # mark the item as played
            self.lastPlayed = id                # update the last played item
            logger.info(f"Started playback of item {id}...")

    def playbackStop(self):
        if not self.allowStop:
            logger.info("Stop requested, but stopping is not allowed, ignoring")
            return
        if not self.player.playing():
            logger.info("Stop requested, but player is not playing")
        if self.player.stop():                  # stop the playback
            if self.playingWidget is not None:
                self.playingWidget.setStopped() # notify the widget, that the playback has stopped
            self.playingWidget = None
            logger.info("Player stopped")


