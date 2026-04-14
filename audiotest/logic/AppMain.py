
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
    def __init__(self, test : Test, testDir : str, argv=[], parent=None):
        super().__init__(parent)
        
        self.test = test
        self.settings = test.settings
        self.language = test.language
        self.testDir = testDir

        reaperPath = self.test.reaper
        if not os.path.isabs(reaperPath):
            reaperPath = os.path.join(self.testDir, reaperPath)
        projectPath = self.test.project
        if not os.path.isabs(projectPath):
            projectPath = os.path.join(self.testDir, projectPath)

        self.app = QApplication(argv)
        self.testWidget = TestWidget(test)
        self.testWidget.endTest.connect(self.endTest)                                           # connect the End Test button signal
        self.window = Window(self.testWidget, test.title, test.theme, onClose=self.endTest)     # connect the window close event too
        self.player = Player(volume=self.settings.volume / 100, reaperPath=reaperPath, projectPath=projectPath)
        self.playback = PlaybackControl(self.player, self.window, inOrder=self.settings.listenInOrder, allowRepeat=self.settings.allowReplay, allowStop=self.settings.allowStop)
        self.ratingLock = RatingLockLogic(self.playback, self.window, rateAny=self.settings.rateAny, rateAfter=self.settings.rateAfter)
        self.resultCollector = ResultCollector(self.test, self.test.title)

        self.player.reaperError.connect(lambda: QMessageBox.warning(self.window, self.language.warningBoxTitle, self.language.reaperError))

    def run(self) -> int:
        self.window.showMaximized()
        QTimer.singleShot(10, self.player.initReaper)  # Initialize Reaper when UI is ready
        logger.info("Running the application")
        ret = self.app.exec()
        if ret != 0:
            logger.error(f"Application finished with exit code {ret}")
        else:
            logger.info(f"Application finished successfully with exit code {ret}")
        return ret

    def saveResults(self) -> bool:
        filename = self.test.results
        if not os.path.isabs(filename):
            filename = os.path.join(self.testDir, filename)
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
