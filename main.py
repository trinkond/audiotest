""" Simple main file to run the whole app """

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import os
import sys

from audiotest.logic.AppMain import AppMain
from audiotest.structure.Test import Test, loadTest

try:
    testFile = sys.argv[1]
    logger.info(f'Starting audio test from "{testFile}"')
except IndexError:
    logger.error("No test file provided, exiting")
    sys.exit(1)

test = loadTest(testFile)

if test is None:
    logger.error("Failed to load the test, exiting...")
    sys.exit(101)
logger.info("Test loaded successfully, running the application...")

app = AppMain(test, argv=sys.argv[2:])
sys.exit(app.run())
