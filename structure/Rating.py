import logging
logger = logging.getLogger(__name__)

class Rating:
    """ Class representing a rating scale """
    def __init__(self, id : str = None):
        self.id = id
    
    TYPE = None

    def __repr__(self):
        id = "" if self.id is None else str(self.id)
        return f'Rating {id}'

    def __str__(self):
        return repr(self)

class RatingDiscrete(Rating):

    def __init__(self, values : dict[int, str], id : str = None):
        super().__init__(id)
        self.scale = sorted((int(k), str(v)) for k, v in values.items())
    
    TYPE = "discrete"

    def __repr__(self):
        id = "" if self.id is None else str(self.id)
        scale = [f'{k}:"{v}"' for k, v in self.scale]
        return f"RatingDiscrete {id}(values=({', '.join(scale)}))"

    def __str__(self):
        return repr(self)

    def value_label(self, val: int) -> str:
        """ returns the label of the value, if not found, returns None """
        for k, v in self.scale:
            if k == val:
                return v
        return None

    def label_value(self, label: str) -> int:
        """ returns the value of the label, if not found, returns None """
        for k, v in self.scale:
            if v == label:
                return k
        return None

class RatingContinuous(Rating):
    
    def __init__(self, minval : int, maxval : int, id : str = None):
        super().__init__(id)
        self.minval, self.maxval = int(minval), int(maxval)
        if self.minval > self.maxval:
            raise ValueError(f"min rating ({self.minval}) is greater than max ({self.maxval})")

    TYPE = "continuous"

    def __repr__(self):
        id = "" if self.id is None else str(self.id)
        return f"RatingContinuous {id}(min={self.minval}, max={self.maxval})"

    def __str__(self):
        return repr(self)

def parseRating(data : dict, id = None) -> Rating:
    """ parses a rating from the data json format into Rating object, returns None if invalid """
    try:
        rtype = str(data["type"])
    except KeyError:
        logger.error(f'Rating {str(id) + " " if id is not None else ""}cannot be parsed, missing "type" key')
        return None

    if rtype == RatingDiscrete.TYPE:
        try:
            values = data.copy()
            values.pop("type")
            return RatingDiscrete(values, id)
        except (TypeError, ValueError, KeyError):
            logger.error(f'Error parsing rating {str(id) if id is not None else ""}')
            return None

    elif rtype == RatingContinuous.TYPE:
        try:
            minval = data["min"]
            maxval = data["max"]
            return RatingContinuous(minval, maxval, id)
        except (KeyError, TypeError, ValueError):
            logger.error(f'Error parsing rating {str(id) if id is not None else ""}')
            return None

    else:
        logger.error(f'Rating {str(id) + " " if id is not None else ""}is unknown type "{rtype}"')
        return None

def parseRatings(data : dict) -> dict[str, Rating]:
    """ parses all ratings from json dict into Rating objects """
    logger.info(f"Parsing ratings")
    ratings = {}
    cc = 0
    for id, val in data.items():
        id = str(id)
        rat = parseRating(val, id)
        if rat is not None:
            cc += 1
        ratings[id] = rat
    if ratings == {}:
        logger.warning("No ratings were parsed")
    else:
        logger.info(f"Successfully parsed {cc} ratings")
    return ratings

def saveRatings(ratings : dict[str, Rating]) -> dict:
    """ formats the Ratings as a dict for saving as json """
    logger.info("Saving ratings")
    data = {}
    for id, rat in ratings.items():
        if isinstance(rat, RatingContinuous):
            rat_dict = {}
            rat_dict["min"] = rat.minval
            rat_dict["max"] = rat.maxval

        elif isinstance(rat, RatingDiscrete):
            rat_dict = {str(k): v for k, v in rat.scale}

        else:
            logger.warning(f'Rating type "{type(rat)}" cannot to be saved')
            data[str(id)] = None
            continue
        
        rat_dict["type"] = rat.__class__.TYPE
        data[rat.id] = rat_dict
    return data
