# Allows to write/read app settings to/from .json


import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from Regions import Region, Sample

def parseRegions(data : dict) -> dict[int, Region]:
    logger.info(f"Parsing regions")
    regions = {}
    cc = 0
    for reg, dat in data.items():
        try:
            reg = int(reg)
        except:
            logger.error(f'Unsupported region ID "{reg}"')
            continue

        dat = Region.fromList(dat)
        if dat is None:
            logger.error(f"Failed to parse region {reg}")
        else:
            cc += 1
        regions[reg] = dat

    if regions == {}:
        logger.warning("No regions were parsed")
    else:
        logger.info(f"Successfully parsed {cc} regions")

    return regions

def parseSamples(data : dict, regions: dict[int, Region]) -> dict[str, Sample]:
    logger.info(f"Parsing samples")
    samples = {}
    cc = 0
    for id, dat in data.items():
        try:
            if type(dat) != list or len(dat) != 2:
                raise Exception()
            track = dat[0]
            regid = dat[1]
        except:
            logger.error(f'Sample "{id}" is in incompatible format')
            continue
        try:
            region = regions[int(regid)]
            cc += 1
        except:
            logger.warning(f'Region {regid} needed by sample "{id}" not found')
            region = None

        samples[id] = Sample(track, region)

    if samples == {}:
        logger.warning("No samples were parsed")
    else:
        logger.info(f"Successfully parsed {cc} samples")
    return samples

def validateRegions(regs : dict[int, Region]) -> bool:
    valid = True
    for key, val in regs.items():
        if type(key) != int or type(val) != Region:
            logger.warning(f"Region {key} not valid, found {val}")
            valid = False
    return valid

def validateSamples(samples : dict[str, Sample]) -> bool:
    valid = True
    for id, val in samples.items():
        if type(id) != str or type(val) != Sample:
            logger.warning(f'Sample "{id}" not valid, found {val}')
            valid = False
    return valid

config_defuault = {
    "version" : None,
    "title" : None,
    "volume" : 100,

    ##language : "EN",

    "regions" : None,
    "samples" : None,
    "ratings" : None,
    "groups" : [],



}

def loadTest(fname : str) -> dict:
    """ Reads the .json configuration file for a test """

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

    config = config_default | data

### Regions
    regs = config["regions"]
    if regs is None:
        logger.error(f'Missing "regions" entry in the test config')
        regs = {}
    else:
        regs = parseRegions(regs)

### Samples
    samples = config["samples"]
    if samples is None:
        logger.error(f'Missing "samples" entry in the test config')
        samples = {}
    else:
        samples = parseSamples(samples)





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











