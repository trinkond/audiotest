# Written by Ondrej Trinkewitz

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

import random

from ..structure.Test import Test
from ..structure.Language import Language, LanguageDefault
from ..structure.Settings import Settings, SettingsDefault
from .SampleWidget import SampleWidget
from .QuestionWidget import QuestionWidget
from .ItemWidget import ItemWidget

class EndButton(QPushButton):
    def __init__(self, text : str = LanguageDefault.endTest, parent=None):
        super().__init__(text=text, parent=parent)

class TestWidget(QWidget):
    """  A widget to represent the whole test as a list of items (samples with questions) """
    def __init__(self, test : Test, parent=None):
        super().__init__(parent)

        self.test = test                    # reference to the test
        settings = test.settings
        language = test.language

        self.itemWidgets = []
        id = 0      # item index for playback and result identification
        dispid = 1  # index for display
        for playlist in self.test.playlists:
            items = []
            for sample in playlist.samples:
                if settings.showSampleNames and sample.id:
                    name = str(sample.id)
                else:
                    name = language.sample + " " + str(dispid)
                    dispid += 1
                item = ItemWidget(sample, playlist.instructions, playlist.questions, sampleName=name, summary=settings.showRatings, id=id)
                items.append(item)
                id += 1
            if settings.shuffleSamples:
                random.shuffle(items)
            self.itemWidgets.extend(items)

        endButton = EndButton(language.endTest)

        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        first = True
        for item in self.itemWidgets:
            if first:
                item.setOpened()
                first = False
            layout.addWidget(item)
            item.expanded.connect(self.itemOpened)
        layout.addWidget(endButton)

        self.setLayout(layout)

    def itemOpened(self, expandedItem):
        for item in self.itemWidgets:
            if item is not expandedItem:
                item.setClosed()
