
import logging
logger = logging.getLogger(__name__)

import os

from ..structure.Settings import Settings
from ..structure.Test import Test
from ..visuals.TestWidget import TestWidget
from ..visuals.Window import Window
from ..player.Player import Player
from .PlaybackControl import PlaybackControl
from .RatingLockLogic import RatingLockLogic
from .ResultCollector import ResultCollector

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QObject, QTimer

class AppMain(QObject):
    """ The main logic of the application """
    def __init__(self, test : Test, reaper = None, project = None, address = None, results = "results.csv", parent=None):
        super().__init__(parent)
        
        self.test = test
        self.settings = test.settings
        self.language = test.language
        self.results = results

        self.app = QApplication([])
        self.testWidget = TestWidget(test)
        self.testWidget.endTest.connect(self.endTest)                                           # connect the End Test button signal
        self.window = Window(self.testWidget, test.title, test.theme, onClose=self.endTest)     # connect the window close event too
        self.resultCollector = ResultCollector(self.test, self.window, self.test.title)
        self.player = Player(volume=self.settings.volume / 100, reaperAddress=address, reaperPath=reaper, projectPath=project)
        self.playback = PlaybackControl(self.player, self.window, self.resultCollector, inOrder=self.settings.listenInOrder, allowRepeat=self.settings.allowReplay, allowStop=self.settings.allowStop, requirePrevFill=self.settings.requirePrevFill)
        self.ratingLock = RatingLockLogic(self.playback, self.window, rateAny=self.settings.rateAny, rateAfter=self.settings.rateAfter)

        self.player.reaperError.connect(lambda: QMessageBox.warning(self.window, self.language.warningBoxTitle, self.language.reaperError))

    def run(self) -> int:
        self.player.initReaper()
        logger.info("Running the application")
        self.window.showMaximized()
        ret = self.app.exec()
        # Stop the playback, when the app quits
        self.player.stop()
        if ret != 0:
            logger.error(f"Application finished with exit code {ret}")
        else:
            logger.info(f"Application finished successfully with exit code {ret}")
        return ret

    def saveResults(self) -> bool:
        logger.info(f"Saving results to {self.results}")
        ret = self.resultCollector.saveResults(self.results, overwrite=self.settings.overwriteResults)
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

        if self.saveResults():
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
                self.app.exit(100)
