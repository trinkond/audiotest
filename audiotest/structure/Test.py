
import logging
logger = logging.getLogger(__name__)

import json
import os

from .Sample import Region, Sample
from .Rating import Rating
from .Question import Question
from .Playlist import Playlist
from .Settings import Settings, SettingsDefault
from .Language import Language, LanguageDefault
from .utils import loadDefault
from ..themes.themes import ThemeDefault

class Test:

    def __init__(self, playlists = [], settings = SettingsDefault, language = LanguageDefault, regions = {}, samples = {}, ratings = {}, questions = {}, version = "0.0", title = "Test", theme = ThemeDefault, reaper = "reaper", project = None, results = "results.csv"):
        self.version = version
        self.title = title
        self.theme = theme
        self.reaper = reaper
        self.project = project
        self.results = results
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
        "reaper" : "reaper",
        "project" : None,
        "results" : "results.csv",
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

        regs = {}
        for key, val in config["regions"].items():
            try:
                reg_id = int(key)
            except (TypeError, ValueError):
                logger.error(f'Unsupported region ID "{key}"')
                continue
            regs[reg_id] = Region.fromList(val, reg_id)

        samples = {}
        for key, val in config["samples"].items():
            key = str(key)
            samples[key] = Sample.fromList(val, regs, key)

        ratings = {}
        for key, val in config["ratings"].items():
            key = str(key)
            ratings[key] = Rating.fromDict(val, key)

        questions = {}
        for key, val in config["questions"].items():
            key = str(key)
            questions[key] = Question.fromDict(val, ratings, key)

        playlists = []
        for val in config["playlists"]:
            playlists.append(Playlist.fromDict(val, samples, questions))

        setts = Settings(config["settings"])
        lang = Language(config["language"])
        version = config["version"]
        title = config["title"]
        theme = config["theme"]
        reaper = config["reaper"]
        project = config["project"]

        if type(project) is not str and project is not None:
            logger.error(f"Invalid project type, expected string or None, got {type(project)}. Project set to None.")
            project = None
        results = config["results"]

        return Test(playlists, setts, lang, regs, samples, ratings, questions, version, title, theme, reaper, project, results)

    def toDict(self) -> dict:
        data = {}
        data["version"] = self.version
        data["title"] = self.title
        data["theme"] = self.theme
        data["reaper"] = self.reaper
        data["project"] = self.project
        data["results"] = self.results
        data["settings"] = self.settings.toDict()
        data["language"] = self.language.toDict()
        data["regions"] = {}
        for region in self.regions.values():
            data["regions"][str(region.id)] = region.toList() if region is not None else None
        data["samples"] = {}
        for sample in self.samples.values():
            data["samples"][str(sample.id)] = sample.toList() if sample is not None else None
        data["ratings"] = {}
        for rating in self.ratings.values():
            data["ratings"][str(rating.id)] = rating.toDict() if rating is not None else None
        data["questions"] = {}
        for question in self.questions.values():
            data["questions"][str(question.id)] = question.toDict() if question is not None else None
        data["playlists"] = []
        data["playlists"] = [pl.toDict() for pl in self.playlists]
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

    test = Test.fromDict(data)
    testDir = os.path.dirname(fname)
    if test is None:
        return None

    # Make the paths absolute with respect to the fname loaded
    if not os.path.isabs(test.reaper):
        test.reaper = os.path.join(testDir, test.reaper)
    if not os.path.isabs(test.project):
        test.project = os.path.join(testDir, test.project)
    if not os.path.isabs(test.theme):
        test.theme = os.path.join(testDir, test.theme)
    if not os.path.isabs(test.results):
        test.results = os.path.join(testDir, test.results)

    return test

def saveTest(fname: str, test: Test) -> bool:

    if not fname.endswith(".json"):
        logger.warning(f'Saving test configuration as non-json file "{fname}"')
    else:
        logger.info(f'Saving test configuration as "{fname}"')

    data = test.toDict()

    try:
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except PermissionError:
        logger.error(f'Permission denied while saving "{fname}"')
        return False
    except Exception as e:
        logger.error(f'Failed to save test configuration to "{fname}": {e}')
        return False

    return True
