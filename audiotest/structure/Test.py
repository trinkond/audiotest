
import logging
logger = logging.getLogger(__name__)

import json

from .Sample import parseRegions, parseSamples, saveRegions, saveSamples
from .Rating import parseRatings, saveRatings
from .Question import parseQuestions, saveQuestions
from .Playlist import parsePlaylists, savePlaylists
from .Settings import Settings, SettingsDefault
from .Language import Language, LanguageDefault
from .utils import loadDefault
from ..themes.themes import ThemeDefault

class Test:

    def __init__(self, playlists = [], settings = SettingsDefault, language = LanguageDefault, regions = {}, samples = {}, ratings = {}, questions = {}, version = "0.0", title = "Test", theme = ThemeDefault):
        self.version = version
        self.title = title
        self.theme = theme
        self.regions = regions
        self.samples = samples
        self.ratings = ratings
        self.questions = questions
        self.playlists = playlists
        self.settings = settings
        self.language = language

    def __repr__(self):
        ret = "Audio test:\n"
        for play in self.playlists:
            ret += str(play) + "\n"
        return ret[:-1]

    def __str__(self):
        return repr(self)

    config_default = {
        "version" : "0.0",
        "title" : "Test",
        "theme" : ThemeDefault,
        "settings" : {},
        "language" : {},

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
        setts = config["settings"]
        setts = Settings(setts)
        lang = config["language"]
        lang = Language(lang)
        version = config["version"]
        title = config["title"]
        theme = config["theme"]

        return Test(plays, setts, lang, regs, samples, rats, quests, version, title, theme)

    def toDict(self) -> dict:
        data = {}
        data["version"] = self.version
        data["title"] = self.title
        data["theme"] = self.theme
        data["settings"] = self.settings.toDict()
        data["language"] = self.language.toDict()
        data["regions"] = saveRegions(self.regions)
        data["samples"] = saveSamples(self.samples)
        data["ratings"] = saveRatings(self.ratings)
        data["questions"] = saveQuestions(self.questions)
        data["playlists"] = savePlaylists(self.playlists)
        return data

def loadTest(fname : str) -> Test:
    """ Reads the .json configuration file of a test """

    if not fname.endswith('.json'):
        logger.warning(f'Loading test configuration from a non-json file "{fname}"')
    else:
        logger.info(f'Loading test configuration from "{fname}"')

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
