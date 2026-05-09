
import logging
logger = logging.getLogger(__name__)

from .utils import loadDefault

class Settings:
    """ Global settings for the application """

    config_default = {
        "volume" : 50,
        "show sample names" : False,
        "shuffle samples" : False,
        "listen in order" : False,
        "allow replay" : True,
        "show ratings" : True,
        "rate any" : True,
        "rate after" : False,
        "require fill all" : False,
        "allow stop" : True,
        "overwrite results" : False,
        "require fill previous" : False
    }

    def __init__(self, data : dict):        
        config = loadDefault(data, Settings.config_default)
        self.volume = config["volume"]
        self.showSampleNames = config["show sample names"]
        self.shuffleSamples = config["shuffle samples"]
        self.listenInOrder = config["listen in order"]
        self.allowReplay = config["allow replay"]
        self.showRatings = config["show ratings"]
        self.rateAny = config["rate any"]
        self.rateAfter = config["rate after"]
        self.requireFillAll = config["require fill all"]
        self.allowStop = config["allow stop"]
        self.overwriteResults = config["overwrite results"]
        self.requirePrevFill = config["require fill previous"]

    def toDict(self) -> dict:
        data = {}
        data["volume"] = self.volume
        data["show sample names"] = self.showSampleNames
        data["shuffle samples"] = self.shuffleSamples
        data["listen in order"] = self.listenInOrder
        data["allow replay"] = self.allowReplay
        data["show ratings"] = self.showRatings
        data["rate any"] = self.rateAny
        data["rate after"] = self.rateAfter
        data["require fill all"] = self.requireFillAll
        data["allow stop"] = self.allowStop
        data["overwrite results"] = self.overwriteResults
        data["require fill previous"] = self.requirePrevFill
        return data

SettingsDefault = Settings(Settings.config_default)
