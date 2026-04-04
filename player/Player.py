# Inspired by Tomas Dudacek in project /mushra_py_ctu
# Written by Ondrej Trinkewitz

import logging
logger = logging.getLogger(__name__)

from audiomath import SystemVolume
from ..structure.Sample import Region, Sample
from PyQt6.QtCore import pyqtSignal, QObject, QTimer

from .ReaperAPI import ReaperAPI, ReaperError, ADDRESS

class Player(QObject):
    """ Audio player interface for playing tracks using Reaper """

    finished = pyqtSignal()

    def __init__(self, reaperAddress : str = ADDRESS, volume : float = 1.0, parent=None):
        super().__init__(parent)
        self.track = 0
        self.region = None
        self.reaperAddress = reaperAddress
        self.volume = volume
        self.reaper = None

        self.REAPER_DELAY = 0.2  # time delay for reaper connection

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.finished.emit)

    def initReaper(self) -> bool:
        """ Initializes the player, must be called before playing any sample """
        logger.info("Initializing the player...")
        try:
            self.reaper = ReaperAPI(self.reaperAddress)
            self.reaper.command(
                self.reaper.Stop,
                self.reaper.Go_to_beginning,
                self.reaper.Unmute_all,
                self.reaper.Unsolo_all,
            )
        except ReaperError as e:
            logger.error(f"Failed to initiate the connection to Reaper: {e}")
            return False
        self.setVolume(self.volume)
        logger.info("Player initialized successfully")
        return True

    def playTrack(self, track : int, region : Region) -> bool:
        if self.reaper is None:
            logger.error("Player not initialized, call initReaper() first")
            return False
        if region is None:
            logger.error("Failed to play, no region provided")
            return False
        if not track in range(1, self.reaper.n_tracks+1):
            logger.error(f"Failed to play, track {track} is out of range")
            return False

        self.setVolume(self.volume)
        try:
            self.reaper.command(
                self.reaper.Unmute_all,
                self.reaper.Unsolo_all,
                self.reaper.Solo_track(track),
                self.reaper.Go_to_time(region.start_time),
                self.reaper.Play,
                )
        except ReaperError as e:
            logger.error(f"Failed to play region {region if region else ''} on track {track}: {e}")
            return False

        self.timer.start(int((region.duration + self.REAPER_DELAY) * 1000))
        logger.info(f'Playing track {track} {"at region " + str(region) if region else ""}...')
        return True

    def playSample(self, sample : Sample) -> bool:
        if sample is None:
            logger.error("Failed to play, no sample provided")
            return False
        logger.info(f'Playing sample "{sample.id if sample.id else ""}"...')
        return self.playTrack(sample.track, sample.region)

    def stop(self) -> bool:
        if self.reaper is None:
            logger.error("Player not initialized, call initReaper() first")
            return False
        try:
            self.reaper.command(self.reaper.Stop)
        except ReaperError as e:
            logger.error(f"Failed to stop playback: {e}")
            return False
        self.timer.stop()
        logger.info("Playback stopped")
        return True

    def playing(self) -> bool:
        if self.reaper is None:
            logger.warning("Player not initialized, checking playing state is irrelevant")
            return False
        return self.timer.isActive()

    def setVolume(self, volume : float):
        try:
            SystemVolume.SetVolume(level=volume, mute=False)
            self.volume = volume
        except Exception as e:
            logger.warning(f"Failed to set system volume to {volume}: {e}")
        logger.info(f"Set volume to {self.volume}")
