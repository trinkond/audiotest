
import logging

logger = logging.getLogger(__name__)

from .Sample import Sample
from .Question import Question

class Playlist:
    """ Representation of a test playlist
    Each playlist contains multiple Samples and
    a set of instructions and questions that are asked for each of the samples """
    def __init__(self, samples : list[Sample], instructions : str, questions : list[Question], reorder=False, name : str = None):
        self.samples = list(samples)
        self.instructions = str(instructions)
        self.questions = list(questions)
        self.reorder = reorder
        self.name = name

    def __repr__(self):
        name = "" if self.name is None else " " + str(self.name)
        ret = f"Playlist{name}:\n"
        ret += "  Samples:\n"
        for sample in self.samples:
            ret += "    " + str(sample) + "\n"
        ret += "  Instructions:\n"
        ret += "    " + str(self.instructions) + "\n"
        ret += "  Questions:\n"
        for quest in self.questions:
            ret += "    " + str(quest) + "\n"
        return ret

    def __str__(self):
        return repr(self)

    @staticmethod
    def fromDict(data : dict, samples : dict[str, Sample], questions : dict[str, Question]):
        """ Constructs a Playlist from a data loaded as dict from a json file
        missing dependencies are filled with None """
        try:
            name = str(data["name"])
        except (KeyError, TypeError, ValueError):
            logger.error(f"Failed to parse name of the playlist {data}")
            return None
        try:
            reorder = bool(data["reorder"])
        except (KeyError, TypeError, ValueError):
            reorder = False
        try:
            instructs = str(data["instructions"])
        except (KeyError, TypeError, ValueError):
            logger.warning(f'Failed to parse the instructions for the playlist {name or ""}')
            instructs = None
        try:
            samps = data["samples"]
            if type(samps) != list:
                raise TypeError()     
        except (KeyError, TypeError, ValueError):
            logger.warning(f'Failed to parse playlist {name or ""}, missing or invalid "samples" entry')
            samps = []
        osamps = []
        for s in samps:
            try:
                s = samples[s]
            except (KeyError, TypeError):
                logger.warning(f'Sample {s} needed by Playlist {name or ""}not found')
                s = None
            osamps.append(s)
        samps = osamps
        try:
            quests = data["questions"]
            if type(quests) != list:
                raise TypeError()
        except (KeyError, TypeError, ValueError):
            logger.warning(f'Failed to parse playlist{name or ""}, missing or invalid "questions"')
            quests = []
        oquests = []
        for q in quests:
            try:
                q = questions[q]
            except KeyError:
                logger.warning(f'Question {q} needed by Playlist {name or ""}not found')
                q = None
            oquests.append(q)
        quests = oquests
        return Playlist(samps, instructs, quests, reorder, name)

def parsePlaylists(data : list, samples : dict[str : Sample], questions : dict[str : Question]) -> list[Playlist]:
    """ parses a list loaded from json into a list of Playlists """
    logger.info("Parsing playlists")
    plays = []
    cc = 0
    for val in data:
        pl = Playlist.fromDict(val, samples, questions)
        if pl is not None:
            cc += 1
            plays.append(pl)
    if plays == {}:
        logger.warning("No playlists were parsed")
    else:
        logger.info(f"Successfully parsed {cc} playlists")
    return plays

def savePlaylists(playlists : list[Playlist]) -> list:
    """ formats the Playlist as a list for saving as json """
    logger.info("Saving playlists")
    data = []
    for pl in playlists:
        pl_dict = {}
        pl_dict["name"] = pl.name
        pl_dict["samples"] = [s.id for s in pl.samples]
        if pl.reorder:
            pl_dict["reorder"] = True
        pl_dict["instructions"] = pl.instructions
        pl_dict["questions"] = [q.id for q in pl.quesions]
        data.append(pl_dict)
    return data
