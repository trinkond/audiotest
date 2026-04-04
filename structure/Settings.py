
import logging
logger = logging.getLogger(__name__)

from .utils import loadDefault

class Settings:
    """ Global settings for the application """

    config_default = {
        "volume" : 50,
        "show sample names" : False,
        "shuffle samples" : False,
        "listen in order" : True,
        "allow replay" : False,
        "show ratings" : True,
        "rate after listening" : True,
        "allow rating change" : False,
        "require fill all" : True,
        "allow stop" : True
    }

    def __init__(self, data : dict):        
        config = loadDefault(data, Settings.config_default)
        self.volume = config["volume"]
        self.showSampleNames = config["show sample names"]
        self.shuffleSamples = config["shuffle samples"]
        self.listenInOrder = config["listen in order"],
        self.allowReplay = config["allow replay"],
        self.listenInOrder = config["listen in order"]
        self.allowReplay = config["allow replay"]
        self.showRatings = config["show ratings"]
        self.rateAfterListening = config["rate after listening"]
        self.allowRatingChange = config["allow rating change"]
        self.requireFillAll = config["require fill all"]
        self.allowStop = config["allow stop"]

    def toDict(self) -> dict:
        data = {}
        data["volume"] = self.volume
        data["show sample names"] = self.showSampleNames
        data["shuffle samples"] = self.shuffleSamples
        data["listen in order"] = self.listenInOrder
        data["allow replay"] = self.allowReplay
        data["show ratings"] = self.showRatings
        data["rate after listening"] = self.rateAfterListening
        data["allow rating change"] = self.allowRatingChange
        data["require fill all"] = self.requireFillAll
        data["allow stop"] = self.allowStop
        return data

SettingsDefault = Settings(Settings.config_default)
