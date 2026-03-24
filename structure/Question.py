### Written by Ondrej Trinkewitz

import logging
logger = logging.getLogger(__name__)

from .Rating import Rating, RatingContinuous, RatingDiscrete

class Question:
    """ class representing question given to the listeners """
    def __init__(self, text : str, rating : Rating, id : str = None):
        self.text = text
        self.rating = rating
        self.id = id

    def __repr__(self):
        id = "" if self.id is None else str(self.id)
        return f'Question {id}(text="{self.text}", rating={self.rating})'

    def __str__(self):
        return repr(self)

def parseQuestion(data : dict, ratings : dict[str, Rating], id : str = None) -> Question:
    """ parse a question from data json format into Question object
    resolves reference to the rating of the question """
    try:
        text = str(data["text"])
    except KeyError:
        logger.warning(f'Question {str(id) + " " if id is not None else ""}is missing "text"')
        text = None
    try:
        rating = str(data["rating"])
        rating = ratings[rating]
        if rating is None:
            raise ValueError()
    except (KeyError, ValueError):
        logger.warning(f'Question {str(id) + " " if id is not None else ""}has "rating" missing or invalid')
        rating = None
    return Question(text, rating, id)

def parseQuestions(data : dict, ratings : dict[str, Rating]) -> dict[str, Question]:
    """ parses json formatted questions to Question objects
    matches and adds ratings, if not found, puts None """
    logger.info(f"Parsing questions")
    questions = {}
    cc = 0
    for id, val in data.items():
        id = str(id)
        qst = parseQuestion(val, ratings, id)
        if qst is not None:
            cc += 1
        questions[id] = qst
    if questions == {}:
        logger.warning("No questions were parsed")
    else:
        logger.info(f"Successfully parsed {cc} questions")
    return questions

def saveQuestions(questions : dict[str, Question]) -> dict:
    """ formats the Samples as a dict for saving into json """
    logger.info("Saving questions")
    data = {}
    for qst in quesions.values():
        qst_dict = {}
        qst_dict["text"] = qst.text
        qst_dict["rating"] = qst.rating.id
        data[str(qst.id)] = qst_dict
    return data
