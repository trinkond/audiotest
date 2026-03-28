""" Testing the loading of the test from .json file """

import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ..structure.Test import Test, loadTest

fname = "./audiotest/tests/sample_settings.json"

test = loadTest(fname)
print(test, end="")

