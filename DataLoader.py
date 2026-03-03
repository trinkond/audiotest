# Allows to write/read app settings to/from .json


import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from Regions import Region, Sample, validateRegions, validateSamples

def loadDefault(data : dict, default : dict) -> dict:
    """ Loads data from the dict, filling missing keys with defaults and checking type """
    data = default | data   # joining the dictionaries
    for key in default:
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

    "regions" : None,
    "samples" : None,
    "questions" : None,
    "ratings" : None,

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

    config = loadDefault(data, config_default)

### Regions
    regs = config["regions"]
    if regs is None:
        logger.error(f'Missing "regions" entry in the test configuration')
        regs = {}
    else:
        regs = parseRegions(regs)

### Samples
    samples = config["samples"]
    if samples is None:
        logger.error(f'Missing "samples" entry in the test configuration')
        samples = {}
    else:
        samples = parseSamples(samples, regions)





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











