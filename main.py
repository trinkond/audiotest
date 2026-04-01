import logging
logger = logging.getLogger(__name__)

import sys

from structure.Test import Test, loadTest
from visuals.Window import Window
from Player import Player
from logic.PlaybackControl import PlaybackControl
from logic.ResultCollector import ResultCollector

RESULT_FILE = "testresults.csv"

class Settings:
    volume = 0.5

def main():
    try:
        testFile = sys.argv[1]
        logger.info(f'Starting audio test from "{testFile}"')
    except IndexError:
        logger.error("No test file provided, exiting")
        return
    try:
        resultFile = sys.argv[2]
        logger.info(f'Results will be saved to "{resultFile}"')
    except IndexError:
        logger.warning(f"No result file provided, results will be saved to {RESULT_FILE}")
        resultFile = RESULT_FILE

    test = loadTest(testFile)

    player = Player(Settings.volume)
    playControl = PlaybackControl(test, player)
    resultCollector = ResultCollector(test, metadata=None)

    app = Window(test)

    playControl.registerSamplesRecursive(app)       # connect the playback control to the app signals
    resultCollector.registerItemsRecursive(app)     # connect the result collector too

    app.show()
    ret = app.exec()

    resultCollector.saveResults(resultFile)

    sys.exit(ret)




