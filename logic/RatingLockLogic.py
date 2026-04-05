
import logging
logger = logging.getLogger(__name__)

from PyQt6.QtCore import QObject, pyqtSignal
from ..visuals.ItemWidget import ItemWidget
from .PlaybackControl import PlaybackControl

class RatingLockLogic(QObject):
    """ Class holding the logic for locking the ratings of the samples """

    def __init__(self, playback : PlaybackControl, object : QObject, rateAny = True, rateAfter = False, parent=None):
        super().__init__(parent)

        self.playback = playback
        self.object = object

        self.rateAny = rateAny
        self.rateAfter = rateAfter

        if self.rateAfter or not self.rateAny:
            # if there are constraints on the rating, update the locks on every playback start and end
            self.playback.playbackBegin.connect(lambda _: self.lockAllRecursive(self.object))
            self.playback.playbackEnd.connect(lambda _: self.lockAllRecursive(self.object))
            self.lockAllRecursive(self.object)
        logger.info(f'Initialized rating lock logic with {"free rating" if rateAny else "current item rating"} and {"rating only after playback" if rateAfter else "rating during playback allowed"}')

    def lockItem(self, item : ItemWidget):
        """ Locks the item based on the settings and current state """

        if self.rateAfter and self.playback.isPlaying():    # rating allowed only after the playback ends
            item.lockRating()
            return

        if not self.rateAny:                                # only allow rating of the currently played item
            if item.id == self.playback.lastPlayed:         # if the item is the current one
                item.unlockRating()
            else:
                item.lockRating()
            return

        item.unlockRating()                                # if free rating, unlock all ratings

    def lockAllRecursive(self, object : QObject):
        """ Locks / unlocks all the items in the object tree based on the settings and current state """
        if isinstance(object, ItemWidget):
            self.lockItem(object)
        for child in object.findChildren(QObject):
            self.lockAllRecursive(child)
