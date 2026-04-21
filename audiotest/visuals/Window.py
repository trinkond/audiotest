
import logging
logger = logging.getLogger(__name__)

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PyQt6.QtCore import Qt, QSize
from ..structure.Test import Test
from .TestWidget import TestWidget
from ..themes.themes import ThemeDefault

class Window(QWidget):
    """ The main window of the test app allowing for scrolling """

    def __init__(self, test : TestWidget, title="Audio test", theme=ThemeDefault, onClose=None, parent=None):
        super().__init__(parent)

        self.testWidget = test
        self.onClose = onClose

        self.scrollWidget = QScrollArea()
        self.scrollWidget.setWidget(self.testWidget)
        self.scrollWidget.setWidgetResizable(True)
        self.scrollWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))
        layout.addWidget(self.scrollWidget)

        self.setLayout(layout)
        self.setMinimumWidth(self.minimumSizeHint().width())

        self.setWindowTitle(title)

        try:
            with open(theme, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            logger.error(f'Failed to load theme, file "{theme}" not found')
        except Exception as e:
            logger.error(f'Failed to load theme from "{theme}", unexpected error: {e}')

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

    def closeEvent(self, event):
        """ Handle window close event """
        if self.onClose:        # if on close function was provided
            self.onClose()      # call it
            event.ignore()      # ignore the close event
        else:
            event.accept()      # accept the close event and close the window
            