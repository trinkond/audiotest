# Written by Ondrej Trinkewitz

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

from ..structure.Test import Test
from .SampleWidget import SampleWidget
from .QuestionWidget import QuestionWidget
from .ItemWidget import ItemWidget

END_THE_TEST = "Finish the test"

class EndButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(text=END_THE_TEST, parent=parent)

class TestWidget(QWidget):
    """  A widget to represent the whole test as a list of items (samples with questions) """
    def __init__(self, test : Test, parent=None):
        super().__init__(parent)

        self.test = test                    # reference to the test

        self.itemWidgets = []
        for pi, playlist in enumerate(self.test.playlists):
            for si, sample in enumerate(playlist.samples):
                item = ItemWidget(sample, playlist.instructions, playlist.questions, id=si, playlist=pi)
                self.itemWidgets.append(item)

        endButton = EndButton()

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
