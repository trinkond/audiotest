# Written by Ondrej Trinkewitz
# Holds the object widgets for the visual user interface

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLineEdit
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QStyle, QStyleOptionSlider
from PyQt6.QtCore import Qt, QSize, pyqtSignal

import math

from Samples import Sample
from Questions import Question, Rating

class SampleWidget(QWidget):
    def __init__(self, sample : Sample):
        super().__init__()

        self.sample = sample   # store reference to the sample object

        label = QLabel(sample.id)
        play_button = QPushButton("Play")

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(play_button)

        self.setLayout(layout)


class LabeledSlider(QWidget):
    
    valueChanged = pyqtSignal(object)
    
    def __init__(self, minimum, maximum, step, parent=None):
        """ slider allowing for float values and custom step,
        displays with labels underneath the slider """
        assert maximum > minimum
        super().__init__(parent)
        self.minval = minimum
        self.maxval = maximum
        self.step = step
        self.n_steps = int(round((self.maxval - self.minval) / self.step))
        self.ticks = []                         # labeled ticks displayed on the slider
        self.SLIDER_OFFSET = self.fontMetrics().horizontalAdvance("mmmm")
        self.SLIDER_HEIGHT = 100 #px
        self.TICK_HEIGHT = 5 #px
        self.LABEL_OFFSET = 10 #px
        self.LABEL_SPACING = 20 #px

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(0, self.n_steps)
        self.slider.setTickPosition(QSlider.TickPosition.NoTicks)
#TODO -20 neni to co chci
        self.slider.setGeometry(0, 0, self.width(), self.height() - 20)

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
        # Returns the current value
        val = self.slider.value()
        return self.minval + self.step * val

    def setValue(self, val):
        # Map external value to internal slider
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
        print(f"start step {start_step} end at {self.n_steps} with step {tick_step}")
        for i in range(start_step, self.n_steps + 1, tick_step):    # iterate all the slider steps
            ticks.append(self.minval + i*self.step)                 # add the stepped value to the list

        print(ticks)
        return ticks

#TODO dodelat size hinty
    def sizeHint(self):
        return QSize(800, 80)

    def minimumSizeHint(self):
        return self.sizeHint()

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

class RatingWidget(QWidget):
    def __init__(self, minimum=0, maximum=100, step = 1):
        super().__init__()

        #self.rating = rating

        layout = QHBoxLayout()

        slider = LabeledSlider(minimum, maximum, step)
        slider.setMaximumWidth(900)  # slider won't grow past 300px

        value_field = QLineEdit()
        value_field.setReadOnly(True)
        value_field.setText(str(slider.value()))
        value_field.setFixedWidth(80)  # fixed width 80px

        slider.valueChanged.connect(lambda v: value_field.setText(str(v)))

        layout.addWidget(slider)
        layout.addWidget(value_field)

        self.setLayout(layout)



class QuestionWidget(QWidget):
    def __init__(self, question : Question):
        super.__init__()

        self.question = question

        label = QLabel(question.id)
        