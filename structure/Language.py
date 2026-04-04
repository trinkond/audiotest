
import logging
logger = logging.getLogger(__name__)

from .utils import loadDefault

class Language:
    """ Language settings """

    default = {
        "sample" : "sample",
        "end test" : "end the test"
    }

    def __init__(self, lang : dict):
        lang = loadDefault(lang, Language.default)
        self.sample = lang["sample"]
        self.endTest = lang["end test"]

    def toDict(self) -> dict:
        data = {}
        data["sample"] = self.sample
        data["end test"] = self.endTest
        return data

LanguageDefault = Language(Language.default)

LanguageEN = Language({
    "sample" : "Track",
    "end test" : "Finish the test"
})

LanguageCZ = Language({
    "sample" : "Stopa",
    "end test" : "Ukončit test"
})

LanguageList = {
    "EN" : LanguageEN,
    "CZ" : LanguageCZ
}
