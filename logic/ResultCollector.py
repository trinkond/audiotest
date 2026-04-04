
import logging
logger = logging.getLogger(__name__)

import os

from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime

from ..visuals.ItemWidget import ItemWidget
from ..structure.Rating import Value
from ..structure.Test import Test

DATE_FORMAT = "%Y-%m-%d %H:%M"      # ISO 8601
VALUE_MISSING = "#MISSING"          # What to export, if an item isn't rated
NO_NAME = "#UNNAMED"                # What to export, if a playlist/sample/question doesn't have a name

def fileExists(fname : str) -> bool:
    """ Check if a file exists """
    return os.path.isfile(fname)

def name(obj) -> str:
    """ Get the name of a playlist/sample/question, or a placeholder if it doesn't have one """
    if hasattr(obj, "name") and obj.name:
        return str(obj.name)
    elif hasattr(obj, "id") and obj.id:
        return str(obj.id)
    else:
        return NO_NAME

def writeList(l : list, label : str | None, csvfile):
    """ Writes a list of values as csv line, optionally with a label at the beginning """
    if label is not None:
        csvfile.write(label + ",")
    csvfile.write(",".join(map(str, l)) + "\n")

class ResultStructure():
    """ A representation of the structure of the test results
    used for generating result headers and data structures """

    def __init__(self, test : Test):
        self.test = test

    def getArray(self, initval : Value = None) -> list[list[list[Value]]]:
        """ generates an empty array for the results with the structure of the test """
        out = []
        for playlist in self.test.playlists:
            playlistData = []
            questionCount = len(playlist.questions)
            for sample in playlist.samples:
                sampleData = [initval] * questionCount
                playlistData.append(sampleData)
            out.append(playlistData)
        return out

    def getItems(self) -> list[tuple[str, str, str]]:
        """ Iterate over all the result items in the test and return their playlist, sample and question ids """
        for playlist in self.test.playlists:
            for sample in playlist.samples:
                for question in playlist.questions:
                    yield (name(playlist), name(sample), name(question))

    def checkFileFormat(self, fname : str, labelFields : int = 1) -> bool:
        """ Test whether a given file has valid result format for the test """

        if not fname.endswith('.csv'):
            logger.warning(f'The file "{fname}" does not have a .csv extension')

        try:
            with open(fname, 'r') as csvfile:
                playlists = csvfile.readline().strip().split(",")
                samples = csvfile.readline().strip().split(",")
                questions = csvfile.readline().strip().split(",")
        except FileNotFoundError:
            logger.error(f'Failed to load the file "{fname}", filename doesn\'t exist')
            return False
        except Exception as e:
            logger.error(f'Failed to load the file "{fname}", error: {e}')
            return False

        logger.info(f'Verifying the format of results in the file "{fname}"')
        loadedItems = zip(playlists[labelFields:], samples[labelFields:], questions[labelFields:])  # skip the labels

        for myStruct, loaded in zip(self.getItems(), loadedItems):
            myPlaylist, mySample, myQuestion = myStruct
            loadedPlaylist, loadedSample, loadedQuestion = loaded

            if myPlaylist.strip().lower() != loadedPlaylist.strip().lower():
                logger.warning(f'Format of the results is invalid: Playlist "{loadedPlaylist}" doesn\'t match test playlist "{myPlaylist}"')
                return False
            if mySample.strip().lower() != loadedSample.strip().lower():
                logger.warning(f'Format of the results is invalid: Sample "{loadedSample}" doesn\'t match test sample "{mySample}"')
                return False
            if myQuestion.strip().lower() != loadedQuestion.strip().lower():
                logger.warning(f'Format of the results is invalid: Question "{loadedQuestion}" doesn\'t match test question "{myQuestion}"')
                return False

        logger.info(f'Format of the file "{fname}" is valid for the test results')
        return True

    def saveHeader(self, fname : str, labelFields : int = 1) -> bool:
        """ Save the result header into a csv file """
        logger.info(f'Printing result header')
        playlists = []
        samples = []
        questions = []
        for play, sample, quest in self.getItems():
            playlists.append(play)
            samples.append(sample)
            questions.append(quest)
        if labelFields > 0:
            playLabel, sampleLabel, questLabel = "Playlist", "Sample", "Question"
            playLabel = playLabel + "," * (labelFields - 1)   # add empty fields for the rest of the labels
            sampleLabel = sampleLabel + "," * (labelFields - 1)
            questLabel = questLabel + "," * (labelFields - 1)
        else:
            playLabel, sampleLabel, questLabel = None, None, None
        try:
            with open(fname, 'w') as csvfile:
                writeList(playlists, playLabel, csvfile)
                writeList(samples, sampleLabel, csvfile)
                writeList(questions, questLabel, csvfile)
        except Exception as e:
            logger.error(f'Failed to save header, error: {e}')
            return False
        return True

class Results:
    """ Stores ratings in a data structure """

    def __init__(self, structure : ResultStructure):
        self.structure = structure
        self.data = structure.getArray()

    def writeRating(self, playlist : int, sample : int, question : int, val : Value):
        """ Write a rating value into the data structure """
        if playlist < 0 or playlist >= len(self.data):
            raise IndexError(f"Playlist index {playlist} out of range")
        if sample < 0 or sample >= len(self.data[playlist]):
            raise IndexError(f"Sample index {sample} out of range")
        if question < 0 or question >= len(self.data[playlist][sample]):
            raise IndexError(f"Question index {question} out of range")

        self.data[playlist][sample][question] = val

    def filled(self):
        """ Check if all ratings have been filled """
        for playlist in self.data:
            for sample in playlist:
                for rating in sample:
                    if rating is None:
                        return False
        return True

    def export(self) -> list[int]:
        """ Export the ratings as a list of values """
        out = []
        for playlist in self.data:
            for sample in playlist:
                for val in sample:
                    out.append(val.value if val is not None else VALUE_MISSING)
        return out

class ResultCollector(QObject):
    """ Collects the ratings inputted by the user
    Connects to the signals of ItemWidget, that yields the rating, sorts and keeps it """

    def __init__(self, test : Test, metadata : str = "Test", parent=None):
        super().__init__(parent)
        logger.info("Initializing the result collector")
        self.test = test
        self.metadata = metadata
        self.metadataItems = self.metadata.count(",") + 1 if self.metadata else 0
        self.structure = ResultStructure(test)
        self.results = Results(self.structure)

    def registerItem(self, item : ItemWidget):
        item.ratingChanged.connect(self.ratingCollect)

    def registerItemsRecursive(self, obj : QObject):
        """ Connect all ItemWidgets in the object tree """
        if isinstance(obj, ItemWidget):
            self.registerItem(obj)
        for child in obj.findChildren(QObject):
            self.registerItemsRecursive(child)

    def ratingCollect(self, val : Value, source : tuple[int, int, int]):
        playlist, sample, question = source
        try:
            self.results.writeRating(playlist, sample, question, val)
        except IndexError as e:
            logger.error(f"Error writing rating: {e}")

    def getResults(self):
        return self.results.export()

    def allFilled(self):
        return self.results.filled()

    def saveResults(self, fname : str, overwrite : bool = False) -> bool:
        """ Save the results into a csv file, with the header and timestamp
        if there is already a file with the given name, the new results will be appended """

        if not self.allFilled():
            logger.warning("Saving results with unfilled ratings")
        if not fname.endswith('.csv'):
            logger.warning(f'Saving results to a non-csv file "{fname}"')
        if fileExists(fname):
            logger.info(f'The file already exists, trying to append the results')
            # check the format to avoid mixing results of different tests
            if self.structure.checkFileFormat(fname, self.metadataItems + 1):   # +1 for the timestamp label
                logger.info(f'Appending test results to the file "{fname}"')
            elif overwrite:
                logger.info(f'Unable to append, overwriting the file "{fname}"')
            else:
                logger.error(f'File format of "{fname}" does not match the current test, nothing was saved')
                return False
        else:
            logger.info(f'Saving test results to a new file "{fname}"')
            # start the new file with the header
            if not self.structure.saveHeader(fname, self.metadataItems + 1):   # +1 for the timestamp label
                return False

        timestamp = datetime.now().strftime(DATE_FORMAT)
        label = timestamp + "," + self.metadata if self.metadata else timestamp
        data = self.getResults()
        try:
            with open(fname, "a") as csvfile:
                writeList(data, label, csvfile)
        except Exception as e:
            logger.error(f'Failed to save results, error: {e}')
            return False
        logger.info(f'Successfully saved results to "{fname}"')
        return True
