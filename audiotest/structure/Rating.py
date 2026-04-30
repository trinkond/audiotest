import logging
logger = logging.getLogger(__name__)

class Rating:
    """ Abstract parent class for representing a rating scale """
    def __init__(self, id : str = None):
        self.id = id

    TYPE = None

    def __repr__(self):
        id = "" if self.id is None else str(self.id)
        return f'Rating {id}'

    def __str__(self):
        return repr(self)

    def toDict(self) -> dict:
        """ returns the Rating data as dict for saving as json """
        raise NotImplementedError("Subclasses must implement toDict()")

    @staticmethod
    def fromDict(data : dict, id : str = None):
        """ constructs a Rating from dict format """
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

class Value:
    """ Storing information about the value and the rating type """
    def __init__(self, rating : Rating, val : int):
        self.rating = rating
        self.value = val
    
    def __str__(self):
        """ Return the text representation of the rating value """
        if type(self.rating) == RatingContinuous:
            return str(self.value)

        elif type(self.rating) == RatingDiscrete:
            for val, label in self.rating.scale:
                if val == self.value:
                    return label
            return ""

        else:
            return "UNKNOWN Rating type"

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

    def toDict(self) -> dict:
        """ returns the RatingDiscrete data as dict for saving as json """
        rat_dict = {str(k): v for k, v in self.scale}
        rat_dict["type"] = self.TYPE
        return rat_dict

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

    def toDict(self) -> dict:
        """ returns the RatingContinuous data as dict for saving as json """
        rat_dict = {}
        rat_dict["min"] = self.minval
        rat_dict["max"] = self.maxval
        rat_dict["type"] = self.TYPE
        return rat_dict

def parseRatings(data : dict) -> dict[str, Rating]:
    """ parses all ratings from json dict into Rating objects """
    logger.info(f"Parsing ratings")
    ratings = {}
    cc = 0
    for id, val in data.items():
        id = str(id)
        rat = Rating.fromDict(val, id)
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
        if rat is None:
            logger.warning(f'Rating {id} is None')
            data[str(id)] = None
            continue
        
        if isinstance(rat, (RatingContinuous, RatingDiscrete)):
            data[rat.id] = rat.toDict()
        else:
            logger.warning(f'Rating type "{type(rat)}" cannot to be saved')
            data[str(id)] = None
    return data
