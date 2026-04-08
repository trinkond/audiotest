""" Testing of my classes Rating in package visuals """

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel
from ..visuals.RatingWidget import RatingWidget, LabeledSlider
from ..structure.Rating import RatingContinuous, RatingDiscrete
import sys

""" Just a dummy widget to showcase the slider supporting float values """
class SliderWidget(QWidget):
    def __init__(self, minimum=0, maximum=100, step = 1):
        super().__init__()

        layout = QHBoxLayout()

        slider = LabeledSlider(minimum, maximum, step)
        slider.setMaximumWidth(900)  # slider won't grow past 300px

        value_field = QLineEdit()
        value_field.setReadOnly(False)
        value_field.setText(str(slider.value()))
        value_field.setFixedWidth(80)  # fixed width 80px

        def update_slider(text):
            try:
                if text:
                    slider.setValue(float(text))
            except ValueError:
                pass

        slider.valueChanged.connect(lambda v: value_field.setText(str(v)))
        value_field.textChanged.connect(update_slider)
        value_field.editingFinished.connect(lambda: value_field.setText(str(slider.value())))

        layout.addWidget(slider)
        layout.addWidget(value_field)

        self.setLayout(layout)


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Rating test")

layout = QVBoxLayout()

# Showcase different slider configurations, including negative values and float values
layout.addWidget(QLabel("Slider examples"))
layout.addWidget(SliderWidget(0,100))
layout.addWidget(SliderWidget(0,1))
layout.addWidget(SliderWidget(-3,54))
layout.addWidget(SliderWidget(12,1000))
layout.addWidget(SliderWidget(-70000,70000))
layout.addWidget(SliderWidget(2,3,0.2))
layout.addWidget(SliderWidget(40, 100, 4))
layout.addWidget(SliderWidget(-2, 34, 3))

# Continuous rating example
layout.addWidget(QLabel("Rating examples"))
layout.addWidget(RatingWidget(RatingContinuous(0, 100)))
layout.addWidget(RatingWidget(RatingContinuous(-5, 5)))

# Discrete rating example
layout.addWidget(RatingWidget(RatingDiscrete({1: "Low", 2: "Medium", 3: "High"})))

window.setLayout(layout)
window.show()

sys.exit(app.exec())

