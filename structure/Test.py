
import logging
logger = logging.getLogger(__name__)

import json

from .Sample import parseRegions, parseSamples, saveRegions, saveSamples
from .Rating import parseRatings, saveRatings
from .Question import parseQuestions, saveQuestions
from .Playlist import parsePlaylists, savePlaylists

def loadDefault(data : dict, default : dict) -> dict:
    """ Loads data from the dict, filling missing keys with defaults and checking type """
    data = data.copy()
    for key in default:
        if not key in data:
            logger.warning(f'Missing entry for "{key}", filled with default value {default[key]}')
            data[key] = default[key]
            continue
        if default[key] is None:
            continue
        if type(data[key]) != type(default[key]):
            logger.error(f'Entry for "{key}" is incompatible format {type(data[key])}, default value {default[key]} has been taken')
            data[key] = default[key]
    return data

class Test:

    def __init__(self, regions, samples, ratings, questions, playlists):
        self.regions = regions
        self.samples = samples
        self.ratings = ratings
        self.questions = questions
        self.playlists = playlists

    def __repr__(self):
        ret = "Audio test:\n"
        for play in self.playlists:
            ret += str(play) + "\n"
        return ret[:-1]

    def __str__(self):
        return repr(self)

    config_default = {
        "version" : None,
        "title" : None,
        "volume" : 100,

        ##language : "EN",

        "regions" : {},
        "samples" : {},
        "questions" : {},
        "ratings" : {},

        "playlists" : [],
    }

    @staticmethod
    def fromDict(data : dict):
        # Load default values for missing entries and check object types
        config = loadDefault(data, Test.config_default)

        regs = config["regions"]
        regs = parseRegions(regs)
        samples = config["samples"]
        samples = parseSamples(samples, regs)
        rats = config["ratings"]
        rats = parseRatings(rats)
        quests = config["questions"]
        quests = parseQuestions(quests, rats)
        plays = config["playlists"]
        plays = parsePlaylists(plays, samples, quests)

        return Test(regs, samples, rats, quests, plays)

    def toDict(self) -> dict:
        data = {}
        data["regions"] = saveRegions(self.regions)
        data["samples"] = saveSamples(self.samples)
        data["ratings"] = saveRatings(self.ratings)
        data["questions"] = saveQuestions(self.questions)
        data["playlists"] = savePlaylists(self.playlists)
        return data

def loadTest(fname : str) -> Test:
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

    return Test.fromDict(data)
