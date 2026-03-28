
from PyQt6.QtCore import QObject, pyqtSignal
from ..visuals.ItemWidget import ItemWidget
from ..structure.Rating import Value


class ResultCollector(QObject):
    """ Collects the ratings inputted by the user
    Connects to the signals of ItemWidget, that yield the rating, sorts and keeps them """

    def __init__(self):
        super().__init__()

        self.ratingList = {}

    def registerItem(self, item : ItemWidget):
        item.ratingChanged.connect(self.ratingCollect)

    def registerItemsRecursive(self, obj : QObject):
        """ Connect all item widgets in the object tree """
        if isinstance(obj, ItemWidget):
            self.registerItem(obj)
        for child in obj.findChildren(QObject):
            self.registerItemsRecursive(child)

    def ratingCollect(self, val : Value, source : tuple[int, int, int]):
        playlist, sample, question = source
        self.ratingList[(playlist, sample, question)] = val
        print(f"Received a rating {val.value} from {source}")





