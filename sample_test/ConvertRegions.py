""" Temporary script to convert regions from .csv exported by Reaper to .json suitable for test files """

import logging
logging.basicConfig(level=logging.INFO)

import sys
import json
from pathlib import Path

# Add the project root to the sys.path to be able to import all the modules
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from structure.Sample import Region, read_config, saveRegions

try:
    regfile = sys.argv[1]
except IndexError:
    regfile = input("Input the name of the region file (csv) exported by Reaper: ")

regions = read_config(regfile)      # Load the regions from the csv file
regions = saveRegions(regions)      # Format the regions as a dict for saving to json

with open(regfile.replace(".csv", ".json"), "w") as f:
    json.dump(regions, f, indent=4)
