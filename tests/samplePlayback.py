""" Testing the Player, playbackController and SampleWidget communication """

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from ..structure.Sample import Sample, Region
from ..visuals.SampleWidget import SampleWidget
from ..logic.PlaybackControl import PlaybackControl
from ..player.Player import Player

player = Player()
if not player.initReaper():
    logger.error("Failed to connect to Reaper, exiting")
    sys.exit(1)
control = PlaybackControl(player)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Playback test")

layout = QVBoxLayout()

reg1 = Region(0.0, 15.778)
reg2 = Region(20.0, 16.209)
samples = [
    Sample(2, reg1),
    Sample(3, reg1),
    Sample(4, reg2),
    Sample(5, reg2)
]

for smpl in samples:
    layout.addWidget(SampleWidget(smpl))

window.setLayout(layout)

# connect all the sample signals to the control object
control.registerSamplesRecursive(window)

window.show()

sys.exit(app.exec())
