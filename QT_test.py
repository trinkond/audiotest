### Sample QT code, chat generated

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

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

window.setLayout(layout)
window.show()

sys.exit(app.exec())

