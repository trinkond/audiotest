""" Simple main file to run the whole app as it goes """

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import sys
from pathlib import Path

# Add the parent of the audiotest package to sys.path so package imports work
PACKAGE_PARENT = Path(__file__).resolve().parents[2]
if str(PACKAGE_PARENT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_PARENT))

from PyQt6.QtWidgets import QApplication
from audiotest.structure.Test import loadTest
from audiotest.visuals.Window import Window
from audiotest.player.Player import Player
from audiotest.logic.PlaybackControl import PlaybackControl
from audiotest.logic.ResultCollector import ResultCollector

RESULT_FILE = "testresults.csv"

class Settings:
    volume = 0.5

try:
    testFile = sys.argv[1]
    logger.info(f'Starting audio test from "{testFile}"')
except IndexError:
    logger.error("No test file provided, exiting")
    sys.exit(1)
try:
    resultFile = sys.argv[2]
    logger.info(f'Results will be saved to "{resultFile}"')
except IndexError:
    logger.warning(f"No result file provided, results will be saved to {RESULT_FILE}")
    resultFile = RESULT_FILE

logger.info("Loading the test...")
test = loadTest(testFile)

logger.info("Initializing the Reaper player...")
player = Player(volume=Settings.volume)
player.initReaper()
playControl = PlaybackControl(player)
resultCollector = ResultCollector(test, metadata=None)

logger.info("Starting the application...")
qtapp = QApplication(sys.argv)
app = Window(test)

playControl.registerSamplesRecursive(app)       # connect the playback control to the app signals
resultCollector.registerItemsRecursive(app)     # connect the result collector too

app.show()
ret = qtapp.exec()

logger.info("Saving the results...")
resultCollector.saveResults(resultFile)

sys.exit(ret)




