# Allows to write/read app settings to/from .json


import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from Regions import Region, Sample, validateRegions, validateSamples
from Questions import Ratings, parseRatings

def loadDefault(data : dict, default : dict) -> dict:
    """ Loads data from the dict, filling missing keys with defaults and checking type """
    data = data.copy()
    for key in default:
        if not key in newdict:
            logger.warning(f'Missing entry for "{key}", filled with default value {default[key]}')
            data[key] = default[key]
            continue
        if default[key] is None:
            continue
        if type(data[key]) != type(default[key]):
            logger.error(f'Entry for "{key}" is incompatible format {type(data[key])}, default value {default[key]} has been taken')
            data[key] = default[key]
    return data

config_default = {
    "version" : None,
    "title" : None,
    "volume" : 100,

    ##language : "EN",

    "regions" : {},
    "samples" : {},
    "questions" : {},
    "ratings" : {},

    "groups" : [],
}



def loadTest(fname : str) -> dict:
    """ Reads the .json configuration file of a test """

    try:
        with open(fname, "r", encoding="utf-8") as f:
            data = json.load(f)

    except FileNotFoundError:
        logger.error(f'Failed to load test configuration, filename "{fname}" not found')
        return None
    except json.JSONDecodeError:
        logger.error(f'Failed to load test configuration, "{fname}" is not a valid .json')
        return None
    except PermissionError:
        logger.error(f'Failed to load test configuration from "{fname}", permission denied')
        return None
    except Exception as e:
        logger.error(f'Failed to load test configuration from "{fname}", unexpected error: {e}')
        return None

    # Load default values for missing entries and check object types
    config = loadDefault(data, config_default)

    regs = config["regions"]
    regs = parseRegions(regs)
    samples = config["samples"]
    samples = parseSamples(samples, regions)
    ratings = config["ratings"]
    ratings = parseRatings(ratings)
    quests = config["questions"]
    quests = parseQuestions(quests)




fname = "sample_settings.json"


with open(fname, "r") as f:
    data = json.load(f)


if "regions" in data:
    regions = parseRegions(data["regions"])
else:
    logger.error("Missing region section")
    regions = {}


print(regions)
print(data["samples"])

samples = parseSamples(data["samples"], regions)

print(samples)











