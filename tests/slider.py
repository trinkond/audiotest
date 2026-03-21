""" Testing of my class LabeledSlider in package visuals """

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit
from ..visuals import LabeledSlider
import sys

""" Just some dummy rating widget for testing the slider """
class RatingWidget(QWidget):
    def __init__(self, minimum=0, maximum=100, step = 1):
        super().__init__()

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

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Slider test")

layout = QVBoxLayout()

layout.addWidget(RatingWidget(0,100))
layout.addWidget(RatingWidget(0,1))
layout.addWidget(RatingWidget(-3,54))
layout.addWidget(RatingWidget(12,1000))
layout.addWidget(RatingWidget(-70000,70000))
layout.addWidget(RatingWidget(2,3,0.2))
layout.addWidget(RatingWidget(40, 100, 4))
layout.addWidget(RatingWidget(-2, 34, 3))

window.setLayout(layout)
window.show()

sys.exit(app.exec())

