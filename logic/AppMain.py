
import logging
logger = logging.getLogger(__name__)

from ..structure.Settings import Settings
from ..structure.Test import Test
from ..visuals.Window import Window
from ..player.Player import Player
from .PlaybackControl import PlaybackControl
from .RatingLockLogic import RatingLockLogic
from .ResultCollector import ResultCollector

from PyQt6.QtWidgets import QApplication

class AppMain():
    """ The main logic of the application """
    def __init__(self, test : Test, argv = []):
        
        self.test = test
        self.settings = test.settings

        self.app = QApplication(argv)
        self.window = Window(test)
        self.player = Player(volume=self.settings.volume / 100)

        self.playback = PlaybackControl(self.player, self.window, inOrder=self.settings.listenInOrder, allowRepeat=self.settings.allowReplay, allowStop=self.settings.allowStop)
        self.ratingLock = RatingLockLogic(self.playback, self.window, rateAny=self.settings.rateAny, rateAfter=self.settings.rateAfter)
        self.resultCollector = ResultCollector(self.test, self.test.title)

    def run(self) -> int:
        logger.info("Starting the player")
        self.player.initReaper()
        self.window.show()
        logger.info("Running the application")
        ret = self.app.exec()
        if ret != 0:
            logger.error(f"Application finished with exit code {ret}")
        else:
            logger.info(f"Application finished successfully with exit code {ret}")
        return ret

    def saveResults(self, filename : str) -> bool:
        logger.info(f"Saving results to {filename}")
        ret = self.resultCollector.saveResults(filename)
        if ret:
            logger.info("Results saved successfully")
        else:
            logger.error("Failed to save the results")
        return ret
        