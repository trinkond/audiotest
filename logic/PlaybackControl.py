
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

    playbackBegin = pyqtSignal(int)     # item ID
    playbackEnd = pyqtSignal(int)       # item ID

    def __init__(self, player : Player, object : QObject, inOrder = False, allowRepeat = True, allowStop = True, parent=None):
        super().__init__(parent)
        self.player = player
        self.object = object
        self.playingWidget = None
        self.inOrder = inOrder
        self.allowRepeat = allowRepeat
        self.allowStop = allowStop

        self.itemPlayed = Checklist()   # Holds if an item has been played for repeat checks
        self.lastPlayed = -1            # Holds the last played item for in order playback

        player.finished.connect(self.playbackFinish)
        self.registerSamplesRecursive(object)   # Connect to the sample widgets in the object tree
        logger.info(f'Initialized PlaybackControl with {"in order playback" if inOrder else "free playback"} and repeat {"allowed" if allowRepeat else "not allowed"}') 

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
            logger.info("Playback requested while player is playing something, ignoring")
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
            self.playbackBegin.emit(id)         # emit the playback begin signal
            logger.info(f"Started playback of item {id}...")

    def playbackFinish(self):
        if self.playingWidget is not None:
            self.playingWidget.setStopped()     # notify the widget, that the playback has stopped
        self.playingWidget = None
        self.playbackEnd.emit(self.lastPlayed)  # emit the playback end signal

    def playbackStop(self):
        if not self.allowStop:
            logger.info("Stop requested, but stopping is not allowed, ignoring")
            return
        if not self.player.playing():
            logger.info("Stop requested, but player is not playing, ignoring")
            return
        if self.player.stop():                      # stop the playback
            self.playbackFinish()                   # run the standard playback ending code
            logger.info("Player stopped")

    def played(self, item : int) -> bool:
        return self.itemPlayed.isChecked(item)

    def lastPlayed(self) -> int:
        return self.lastPlayed

    def isPlaying(self) -> int:
        return self.player.playing()
