""" Simple main file to run the whole app """

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import argparse
import os
import sys

from audiotest.logic.AppMain import AppMain
from audiotest.structure.Test import Test, loadTest

parser = argparse.ArgumentParser(description="Run the audio test")
parser.add_argument("config_file", help="JSON test configuration file")
parser.add_argument("result_file", nargs="?", default="results.csv", help="CSV file path to save results")
parser.add_argument("-r", "--reaper", dest="reaper", help="Path to the Reaper executable")
parser.add_argument("-p", "--project", dest="project", help="Path to the Reaper project file")
parser.add_argument("-a", "--address", dest="address", help="Address of the Reaper interface, normally 127.0.0.1:8080")

args = parser.parse_args()

testFile = args.config_file
if not os.path.isfile(testFile):
    logger.error(f'Test configuration file "{testFile}" not found')
    sys.exit(1)
logger.info(f'Starting audio test from "{testFile}"')

test = loadTest(testFile)
if test is None:
    logger.error("Failed to load the test, exiting...")
    sys.exit(101)

# if the result or project paths are not absolute, make them relative to the test config file
testDir = os.path.dirname(os.path.abspath(testFile))
if not os.path.isabs(args.result_file):
    args.result_file = os.path.join(testDir, args.result_file)
if args.project is not None and not os.path.isabs(args.project):
    args.project = os.path.join(testDir, args.project)

logger.info("Test loaded successfully, running the application...")
app = AppMain(test,
              reaper=args.reaper,
              project=args.project,
              address=args.address,
              results=args.result_file)
sys.exit(app.run())
