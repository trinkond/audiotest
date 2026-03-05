### Written by Ondrej Trinkewitz

import logging
logger = logging.getLogger(__name__)


class Rating:
    """ Class representing a rating scale """
    def __init__(self, id : str = None):
        self.id = id

class RatingDiscrete(Rating):

    def __init__(self, values : dict[int, str], id : str = None):
        super().__init__(id)
        self.scale = sorted((int(k), str(v)) for k, v in values.items())

class RatingContinuous(Rating):
    
    def __init__(self, minval : int, maxval : int, step : int, id :str  = None):
        super().__init__(id)
        self.minval, self.maxval, self.step = int(minval), int(maxval), int(step)
        if self.minval > self.maxval:
            raise ValueError(f"min rating ({self.min}) is greater than max ({self.max})")

def parseRating(data : dict, id = None) -> Rating:
    try:
        rtype = data["type"]
    except KeyError:
        logger.error(f'Rating {str(id) + " " if id is not None else ""}cannot be parsed, missing "type" key')
        return None

    if rtype.lower() == "discrete":
        del data["type"]
        try:
            return RatingDiscrete(data.copy().pop("type"), id)
        except (TypeError, ValueError, KeyError):
            logger.error(f'Error parsing rating {str(id) if id is not None else ""}')
            return None

    elif rtype.lower() == "continuous":
        try:
            min = data["min"]
            max = data["max"]
            step = data["step"]
            return RatingContinuous(min, max, step, id)
        except (KeyError, TypeError, ValueError):
            logger.error(f'Error parsing rating {str(id) if id is not None else ""}')
            return None

    else:
        logger.error(f'Rating {str(id) + " " if id is not None else ""}is unknown type "{rtype}"')
        return None

def parseRatings(data : dict) -> dict[str, Rating]:
    logger.info(f"Parsing ratings")
    ratings = {}
    cc = 0
    for id, val in data.items():
        id = str(id)
        rat = parseRating(val, id)
        if rat is None:
            logger.error(f"Failed to parse rating {id}")
        else:
            cc += 1
        ratings[id] = rat
    if ratings == {}:
        logger.warning("No ratings were parsed")
    else:
        logger.info(f"Successfully parsed {cc} ratings")
    return ratings

class Question:
    """ class representing question given to the listeners """
    def __init__(self, text : str, rating : Rating, forced=True):
        self.text = text
        self.rating = rating
        self.forced = forced

def parseQuestion():
    return None