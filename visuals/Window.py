
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PyQt6.QtCore import Qt, QSize
from ..structure.Test import Test
from .TestWidget import TestWidget

class Window(QWidget):
    """ The main window of the test app allowing for scrolling """

    def __init__(self, test : Test, parent=None):
        super().__init__(parent)

        self.test = test
        self.testWidget = TestWidget(test)

        self.scrollWidget = QScrollArea()
        self.scrollWidget.setWidget(self.testWidget)
        self.scrollWidget.setWidgetResizable(True)
        self.scrollWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("My awesome testing app"))
        layout.addWidget(self.scrollWidget)

        self.setLayout(layout)
        self.setMinimumWidth(self.minimumSizeHint().width())

        self.setWindowTitle(test.title)

    def marginWidth(self) -> int:
        margins = self.layout().contentsMargins()
        width = margins.left() + margins.right()                # add the layout margins
        width += 2 * self.scrollWidget.frameWidth()             # add the scroll area frame (both sides)
        width += self.scrollWidget.verticalScrollBar().sizeHint().width()  # add the scrollbar width
        return width

    def minimumSizeHint(self) -> QSize:
        width = self.testWidget.minimumSizeHint().width()       # fit the full content width
        width += self.marginWidth()                             # add the margins and scrollbar
        width = max(width, super().minimumSizeHint().width())   # make sure it's not smaller than the default minimum
        height = super().minimumSizeHint().height()             # vertical is scrollable, so just default
        return QSize(width, height)

    def sizeHint(self) -> QSize:
        width = self.testWidget.sizeHint().width()
        width += self.marginWidth()
        width = max(width, super().sizeHint().width())
        height = (3 * width) // 4
        height = max(height, super().sizeHint().height())
        return QSize(width, height)
