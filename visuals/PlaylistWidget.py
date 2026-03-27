# Written by Ondrej Trinkewitz

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt

from ..structure.Playlist import Playlist
from .SampleWidget import SampleWidget
from .QuestionWidget import QuestionWidget
from .ItemWidget import ItemWidget


class PlaylistWidget(QScrollArea):
    """  A widget to represent a playlist of items (samples with questions) """
    def __init__(self, playlist : Playlist, parent=None):
        super().__init__(parent)

        self.playlist = playlist   # reference to the playlist
        self.itemWidgets = []
        for i, sample in enumerate(playlist.samples):
            item = ItemWidget(sample, playlist.instructions, playlist.questions, id=i)
            self.itemWidgets.append(item)

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        first = True
        for item in self.itemWidgets:
            if first:
                item.setOpened()
                first = False
            layout.addWidget(item)
            item.expanded.connect(self.itemOpened)

        self.container.setLayout(layout)
        self.setWidget(self.container)

    def itemOpened(self, expandedItem):
        for item in self.itemWidgets:
            if item is not expandedItem:
                item.setClosed()

class ExpandableListWidget(QScrollArea):
    """  A widget to represent a list of items, is scrollable if needed, each item can be expanded"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.container = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(4)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.container.setLayout(self.layout)
        self.setWidget(self.container)

    def addItem(item : ItemWidget):
        self.layout.addWidget(item)
        item.expanded.connect(self.itemOpened)


    def itemOpened(self, expandedItem):
        for item in self.itemWidgets:
            if item is not expandedItem:
                item.setClosed()


