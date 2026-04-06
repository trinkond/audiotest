
import logging
logger = logging.getLogger(__name__)

from ..structure.Settings import Settings
from ..structure.Test import Test
from ..visuals.TestWidget import TestWidget
from ..visuals.Window import Window
from ..player.Player import Player
from .PlaybackControl import PlaybackControl
from .RatingLockLogic import RatingLockLogic
from .ResultCollector import ResultCollector

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QObject

class AppMain(QObject):
    """ The main logic of the application """
    def __init__(self, test : Test, argv=[], parent=None):
        super().__init__(parent)
        
        self.test = test
        self.settings = test.settings
        self.language = test.language

        self.app = QApplication(argv)

        self.testWidget = TestWidget(test)
        self.testWidget.endTest.connect(self.endTest)
        self.window = Window(self.testWidget, test.title, test.theme, onClose=self.endTest)
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
        ret = self.resultCollector.saveResults(filename, overwrite=self.settings.overwriteResults)
        if ret:
            logger.info("Results saved successfully")
        else:
            logger.error("Failed to save the results")
        return ret
    
    def endTest(self):
        if self.settings.requireFillAll and not self.resultCollector.allFilled():
            reply = QMessageBox.question(
                self.window,
                self.language.fillAllErrTitle,
                self.language.fillAllErrMessage,
                QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Cancel
            )
            if reply != QMessageBox.StandardButton.Ok:
                return

        if self.saveResults("audiotest/tests/test_results.csv"):
            self.app.exit(0)
        else:
            reply = QMessageBox.question(
                self.window,
                self.language.saveErrTitle,
                self.language.saveErrMessage,
                QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Ok:
                self.app.exit(0)
