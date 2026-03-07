# Allows to write/read app settings to/from .json


import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from Regions import parseRegions, parseSamples
from Questions import parseRatings, parseQuestions

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

class Playlist:
    """ Representation of a test playlist
    Each playlist contains multiple Samples and
    a set of instructions and questions that are asked for each of the samples """
    def __init__(self, samples : list[Sample], instructions : str, questions : list[Question], reorder=False, name : str = None):
        self.samples = list(samples)
        self.instructions = str(instructions)
        self.questions = list(questions)
        self.reorder = reorder
        self.name = name

    @staticmethod
    def fromDict(data : dict, samples : dict[str, Sample], questions : dict[str, Question]):
        """ Constructs a Playlist from a data loaded as dict from a json file
        missing dependencies are filled with None """
        try:
            name = str(data["name"])
        except (KeyError, TypeError, ValueError):
            logger.error(f"Failed to parse name of the playlist {data}")
            return None
        try:
            reorder = bool(data["reorder"])
        except (KeyError, TypeError, ValueError):
            reorder = False
        try:
            instructs = str(data["instructions"])
        except (KeyError, TypeError, ValueError):
            logger.warning(f'Failed to parse the instructions for the playlist {name or ""}')
            instructs = None
        try:
            samps = data["samples"]
            if type(samps) != list:
                raise TypeError()     
        except (KeyError, TypeError, ValueError):
            logger.warning(f'Failed to parse playlist {name or ""}, missing or invalid "samples" entry')
            samps = []
        osamps = []
        for s in samps:
            try:
                s = samples[s]
            except KeyError:
                logger.warning(f'Sample {s} needed by Playlist {name or ""}not found')
                s = None
            osamps.append(s)
        samps = osamps
        try:
            quests = data["questions"]
            if type(quests) != list:
                raise TypeError()
        except (KeyError, TypeError, ValueError):
            logger.warning(f'Failed to parse playlist{name or ""}, missing or invalid "questions"')
            quests = []
        oquests = []
        for q in quests:
            try:
                q = questions[q]
            except KeyError:
                logger.warning(f'Question {q} needed by Playlist {name or ""}not found')
                q = None
            oquests.append(q)
        quests = oquests
        return Playlist(samps, instructs, quests, reorder, name)

def parsePlaylists(data : list) -> dict[str : Playlist]:
    """ parses a list loaded from json into a list of Playlists """
    logger.info("Parsing playlists")
    plays = []
    for val in data:
        pl = Playlist.fromDict(val)
        if pl is not None:
            cc += 1
            plays.append(pl)
    if plays == {}:
        logger.warning("No playlists were parsed")
    else:
        logger.info(f"Successfully parsed {cc} playlists")
    return plays

def savePlaylists(playlists : dict[str : Playlist]) -> list:
    """ formats the Playlist as a list for saving as json """
    logger.info("Saving playlists")
    data = []
    for pl in playlists.values():
        pl_dict = {}
        pl_dict["name"] = pl.name
        pl_dict["samples"] = [s.id for s in pl.samples]
        if pl.reorder:
            pl_dict["reorder"] = True
        pl_dict["instructions"] = pl.instructions
        pl_dict["questions"] = [q.id for q in pl.quesions]
        data.append = pl_dict
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

    "playlists" : [],
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
    samples = parseSamples(samples, regs)
    rats = config["ratings"]
    rats = parseRatings(rats)
    quests = config["questions"]
    quests = parseQuestions(quests, rats)

    return (samples, quests)




fname = "sample_settings.json"

samples, quests = loadTest(fname)

print(samples)
print(quests)











