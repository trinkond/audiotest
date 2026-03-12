### Sample QT code, chat generated

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from Samples import Region, Sample
from Visuals import SampleWidget, RatingWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Basic Qt UI")

label = QLabel("Hello Qt!")
button = QPushButton("Click me")

def on_click():
    label.setText("Button clicked!")

button.clicked.connect(on_click)

layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)


samples = {
    Sample(1, Region(0.0, 1.0, 1), "Sample1"),
    Sample(2, Region(0.3, 2.9, 3), "Sample2")
}

for sample in samples:
    widget = SampleWidget(sample)
    layout.addWidget(widget)

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

