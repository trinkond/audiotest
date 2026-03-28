from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, QObject, QEvent, Qt

from .SampleWidget import SampleWidget
from .QuestionWidget import QuestionWidget
from ..structure.Sample import Sample
from ..structure.Question import Question
from ..structure.Rating import Value

class ClickWatcher(QObject):
    """ Listens for clicks on a widget including its children and emits a signal when that happens """

    def __init__(self, obj : QObject = None):
        super().__init__()
        if obj:
            self.installRecursive(obj)

    clicked = pyqtSignal(object)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            self.clicked.emit(obj)          # emit the object, that was actually clicked
        return super().eventFilter(obj, event)

    def install(self, obj: QObject):
        obj.installEventFilter(self)

    def installRecursive(self, obj: QObject):
        """ Installs the clickWatcher on a QObject and all its children
        so the click event reacts to all clicks inside the object (including buttons, textfields etc.) """
        self.install(obj)
        for child in obj.children():
            if isinstance(child, QObject):
                self.installRecursive(child)

class ItemWidget(QWidget):
    """ A widget representing an item containing a sample to be played and a list of questions to be filed """
    
    expanded = pyqtSignal(object)                       # emits itself when clicked and expanded
                           # value, ( playlistID, itemID, questionID )
    ratingChanged = pyqtSignal(Value, tuple)            # emit the rating change to for result collection

    def __init__(self, sample : Sample, instructions : str, questions : list[Question], id : int = 0, playlist : int = 0, parent=None, expanded=False):
        super().__init__(parent)
        self.id = id
        self.pl = playlist

        self.instructWidget = QLabel(instructions)
        self.sampleWidget = SampleWidget(sample)
        self.questWidgets = []
        for i, quest in enumerate(questions):
            self.questWidgets.append(QuestionWidget(quest, i))

        self.opened = expanded      # track whether item is in expanded or summary view
        
        self.rating_summary = QWidget()
        rating_layout = QHBoxLayout(self.rating_summary)
        for i, quest in enumerate(self.questWidgets):
            rating_layout.addWidget(QLabel(str(f"Q{i+1}")))

        self.header = QWidget()
        header_layout = QHBoxLayout(self.header)
        header_layout.addWidget(self.sampleWidget)
        header_layout.addWidget(self.rating_summary)
        self.header.setMaximumHeight(60)
        header_layout.setContentsMargins(0, 0, 0, 0)    # leave only main layout margins

        self.body = QWidget()
        body_layout = QVBoxLayout(self.body)
        body_layout.addWidget(self.instructWidget)
        for quest in self.questWidgets:
            body_layout.addWidget(quest)
            quest.ratingChanged.connect(lambda val, quest: self.ratingChanged.emit(val, (self.pl, self.id, quest)))
        body_layout.setContentsMargins(0, 0, 0, 0)      # leave only main layout margins

        layout = QVBoxLayout()
        layout.setSpacing(0)                            # zero spacing between header and body
        layout.addWidget(self.header)
        layout.addWidget(self.body)

        self.setLayout(layout)

        # allow the widget to draw its background and border
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        if self.opened:
            self.setOpened()
        else:
            self.setClosed()

        self.clickWatch = ClickWatcher(self.header)             # listen for clicks on the header
        self.clickWatch.clicked.connect(self.clickResolve)      # connect the click signal to the corresponding function

    def setOpened(self):
        self.opened = True
        self.body.setVisible(True)
        self.rating_summary.setVisible(False)
    
    def setClosed(self):
        self.opened = False
        self.body.setVisible(False)
        self.rating_summary.setVisible(True)

    def clickResolve(self, obj: object):
        """ Expands the item, if the header gets clicked """
        if not self.opened:
            self.setOpened()
            self.expanded.emit(self)    # notify other widgetsabout the expansion

