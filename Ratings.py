### Written by Ondrej Trinkewitz

import logging
logger = logging.getLogger(__name__)




class Rating:
    """ Class representing a rating scale """
    def __init__(id : str = None):
        self.id = id

class RatingDiscrete(Rating):

    def __init__(self, values : dict[int, str], id = None):
        super().__init__()
        self.scale = sorted((int(k), str(v)) for k, v in values.items())



class RatingContinuous(Rating):
    
    def __init__(self, min, max, step, id = None):
        super().__init__()
        self.min, self.max, self.step = int(min), int(max), int(step)
        if self.min > self.max:
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
            return RatingDiscrete(data, id)
        except:
            logger.error(f'Error parsing rating {str(id) if id is not None else ""}')
            return None
        finally:
            data["type"] = "discrete"

    elif rtype.lower() == "continuous":
        try:
            min = data["min"]
            max = data["max"]
            step = data["step"]
            return RatingContinuous(min, max, step, id)
        except:
            logger.error(f'Error parsing rating {str(id) if id is not None else ""}')
            return None

    else:
        logger.error(f'Rating {str(id) + " " if id is not None else ""}is unknown type "{rtype}"')
        return None

def parseRatings(data : dict) -> dict[str, Rating]:
    for id, val in data.items():
        pass

