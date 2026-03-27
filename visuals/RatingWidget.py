# Written by Ondrej Trinkewitz
# Contains the visual part for the Rating class

from PyQt6.QtWidgets import QWidget, QStyle, QLabel, QSlider, QHBoxLayout, QLineEdit, QButtonGroup, QRadioButton, QStyleOptionSlider
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QSize, pyqtSignal

from ..structure.Rating import RatingDiscrete, RatingContinuous, Rating, Value

import math

class Scale(QWidget):
    """ Abstract class for a rating scale """

    valueChanged = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

    def value(self) -> int:
        # Returns the current value
        raise NotImplementedError(f"Class {self.__class__} doesn't implement a function for reading the value")

    def setValue(self, val : int):
        # Map external value to internal slider
        raise NotImplementedError(f"Class {self.__class__} doesn't allo654w to set a value")

class LabeledSlider(Scale):
    """ Slider that supports float values and a custom step,
    renders with automatic labels underneath the slider """
    
    def __init__(self, minimum, maximum, step, parent=None):
        
        assert maximum > minimum
        super().__init__(parent)
        self.minval = minimum
        self.maxval = maximum
        self.step = step
        self.n_steps = int(round((self.maxval - self.minval) / self.step))
        self.ticks = []                         # labeled ticks displayed on the slider
        self.SLIDER_OFFSET = self.fontMetrics().horizontalAdvance("88") # some offset to accommodate labels on the sides
        self.SLIDER_HEIGHT = 20 #px
        self.TICK_HEIGHT = 5 #px
        self.LABEL_OFFSET = 10 #px
        self.LABEL_SPACING = 10 #px

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(0, self.n_steps)
        self.slider.setTickPosition(QSlider.TickPosition.NoTicks)

        self.resizeEvent(None)  # generate the ticks and scales

        # on slider value change emit signal with the new value
        self.slider.valueChanged.connect(lambda _: self.valueChanged.emit(self.value()))

    def _sliderPos(self):
        """ extract and return the positions of the minimum and maximum value of the slider in px """
        # retrive the slider groove and handle
        opt = QStyleOptionSlider()
        self.slider.initStyleOption(opt)
        style = self.slider.style()
        groove = style.subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderGroove, self)
        handle = style.subControlRect(QStyle.ComplexControl.CC_Slider, opt, QStyle.SubControl.SC_SliderHandle, self)

        left = groove.left() + handle.width()//2 + self.SLIDER_OFFSET
        right = groove.right() - handle.width()//2 + self.SLIDER_OFFSET
        y = groove.center().y()

        return int(left), int(right), int(y)

    def _sliderWidth(self):
        left, right, _ = self._sliderPos()
        return right - left

    def value(self):
        val = self.slider.value()
        return self.minval + self.step * val

    def setValue(self, val):
        val = max(min(val, self.maxval), self.minval)   # clamp the value to the slider range
        val = (val - self.minval) / self.step
        self.slider.setValue(int(round(val)))

    def steps(self) -> list:    # returns a list of all the slider steps
        return [self.minval + i * self.step for i in range(self.n_steps + 1)]

    @staticmethod
    def _niceRound(val : float, integer=True):
        """ rounds the number up to the nearest 1/2/5/10 * 10**n """
        exponent = math.floor(math.log10(val))      # step = fraction * 10**exponent
        if integer:                                 # integer=False allows returning of non integers like 0.1, 0.02, 0.0005
            exponent = max(exponent, 0)             # clamp to positive exponents only
        fraction = val / (10 ** exponent)           # fraction in [1, 10], find closest 1/2/5/10
        if fraction <= 1:
            fraction = 1
        elif fraction <= 2:
            fraction = 2
        elif fraction <= 5:
            fraction = 5
        else:
            fraction = 10
        return fraction * (10**exponent)

    def _label_width(self):
        max_label = self.fontMetrics().horizontalAdvance(str(self.maxval))  # estimate the longest possible label
        min_label = self.fontMetrics().horizontalAdvance(str(self.minval))
        label_width = max(min_label, max_label) + self.LABEL_SPACING        # add minimal spacing between labels in px
        return label_width

    def _getTicks(self, max_steps=20):
        """ computes the parameters of labels displayed under the slider 
        based on the current slider width. Displays muliples of 2/5/10 """
        label_width = self._label_width() + self.LABEL_SPACING # add minimal spacing to the label size

        val_range = self.maxval - self.minval
        min_step = val_range * label_width / self._sliderWidth()    # minimal step size to accommodate the labels
        min_step = max(min_step, val_range / max_steps)             # minimal step size to not exceed max_steps

        tick_step = self._niceRound(min_step / self.step)           # round the step to some nice multiple of slider step
        minvalstep = self.minval / self.step                        # is minval divisible by step? e.g. sequence contains 0?
        if math.isclose(minvalstep, round(minvalstep), abs_tol=1e-6):
            minvalstep = int(round(minvalstep))                     # number of steps corresponding to minval
            div = math.ceil(minvalstep / tick_step)
            start_step = int(round(div*tick_step))                  # the first step, divisible by tick_step
            start_step -= minvalstep                                # add the minval offset, so minval ~ 0
        else:                                                       # no hope for divisibility
            start_step = 0                                          # start step is at minval

        ticks = []
        for i in range(start_step, self.n_steps + 1, tick_step):    # iterate all the slider steps
            ticks.append(self.minval + i*self.step)                 # add the stepped value to the list

        return ticks

    def sizeHint(self):
        height = self.SLIDER_HEIGHT + self.LABEL_OFFSET + self.fontMetrics().height()
        return QSize(500, height)

    def minimumSizeHint(self):
        height = self.SLIDER_HEIGHT + self.LABEL_OFFSET + self.fontMetrics().height()
        width = 100 + 2*self.SLIDER_OFFSET
        return QSize(width, height)
        
    def resizeEvent(self, event):
        self.ticks = self._getTicks()                               # recompute the tick marks
        sliderLeft = self.SLIDER_OFFSET
        sliderWidth = self.width() - 2*self.SLIDER_OFFSET
        sliderHeight = self.SLIDER_HEIGHT                           # update slider dimensions
        self.slider.setGeometry(sliderLeft, 0, sliderWidth, sliderHeight)
        self.update()                                               # trigger repaint
        super().resizeEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        fm = self.fontMetrics()                                 # for font sizes
        left, right, y = self._sliderPos()    

        for tick in self.ticks:
            rel = (tick - self.minval) / (self.maxval - self.minval)
            x = int(left + rel*(right - left))                  # compute the x coordinate
            painter.drawLine(x, y, x, y + self.TICK_HEIGHT)     # draw tick line
            label = str(tick)
            painter.drawText(                                   # draw the number label
                x - fm.horizontalAdvance(label)//2,
                y + self.LABEL_OFFSET + fm.ascent(),
                label
            )

class ButtonRow(Scale):
    """ A row of check buttons with labels, one can be selected at a time. """
    
    def __init__(self, options: list[tuple[int, str]], parent=None):
        
        super().__init__(parent)

        layout = QHBoxLayout()
        self.buttons = {}
        self.group = QButtonGroup()
        self.chosen = None

        for i, label in options:
            btn = QRadioButton(label)
            self.buttons[i] = btn
            self.group.addButton(btn, i)
            layout.addWidget(btn)

        # on button press emit signal with the new value
        self.group.buttonClicked.connect(lambda idx: self.valueChanged.emit(self.value()))

        self.setLayout(layout)

    def value(self):
        return self.group.checkedId()

    def setValue(self, val):
        try:
            self.group.button(val).setChecked(True)
        except AttributeError:
            pass

    def sizeHint(self):
        original = super().sizeHint()
        return QSize(original.width() + 200, original.height())

class RatingWidget(QWidget):
    """ Widget for displaying a rating, supports both discrete and continuous ratings
    contains a slider or a row of buttons as input and a text field for diplay """

    ratingChanged = pyqtSignal(Value)  # signal a rating change

    def __init__(self, rating : Rating, parent=None, textEditable=True):
        super().__init__(parent)

        self.rating = rating

        self.valueField = QLineEdit()
        self.valueField.setReadOnly(not textEditable)
        self.valueField.setFixedWidth(80)  # fixed width 80px

        if type(self.rating) == RatingContinuous:
            self.scale = LabeledSlider(int(rating.minval), int(rating.maxval), step=1)
        elif type(self.rating) == RatingDiscrete:
            self.scale = ButtonRow(rating.scale)
        else:
            raise TypeError(f"Invalid rating type {self.type}")

        layout = QHBoxLayout()
        self.scale.setMaximumWidth(900)  # scale won't grow past 900px
        layout.addWidget(self.scale)
        layout.addWidget(self.valueField)

        self.setLayout(layout)

        self.scale.valueChanged.connect(self.valueUpdate)
        if textEditable:
            self.valueField.textChanged.connect(self.parseLabel)
            self.valueField.editingFinished.connect(lambda: self.valueUpdate(self.scale.value()))

    def parseLabel(self, text):
        """ If the label is editted as text """
        try:
            self.scale.setValue(int(text))
        except (TypeError, ValueError):
            pass

    def valueUpdate(self, val):
        """ Update the label shown and send a signal about the change """
        val = Value(self.rating, val)   # pack the raw int into a Value object
        self.ratingChanged.emit(val)
        self.valueField.setText(str(val))
