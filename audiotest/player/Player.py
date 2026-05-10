# Inspired by Tomas Dudacek in project /mushra_py_ctu
# Written by Ondrej Trinkewitz

import logging
logger = logging.getLogger(__name__)

from audiomath import SystemVolume
from ..structure.Sample import Region, Sample
from PyQt6.QtCore import pyqtSignal, QObject, QTimer
import subprocess, time

from .ReaperAPI import ReaperAPI, ReaperError

def launchReaper(reaperPath : str, reaperAddress : str = ReaperAPI.ADDRESS, projectPath : str = None, timeout : float = 5.0) -> bool:
    """ Launches Reaper with the given project, returns True if successful """
    try:
        subprocess.Popen(
            [reaperPath, projectPath] if projectPath else [reaperPath],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=(subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        )
        timeout = time.time() + timeout
        while time.time() < timeout:
            if ReaperAPI.ping_server(reaperAddress):
                logger.info(f'Successfully launched Reaper from "{reaperPath}" with project "{projectPath}"')
                return True
            time.sleep(0.1)
        logger.error(f'Failed to launch Reaper from "{reaperPath}" with project "{projectPath}": timeout')
        return False
    except Exception as e:
        logger.error(f'Failed to launch Reaper from "{reaperPath}" with project "{projectPath}": {e}')
        return False

class Player(QObject):
    """ Audio player interface for playing tracks using Reaper """

    finished = pyqtSignal()
    reaperError = pyqtSignal()

    def __init__(self, volume : float = 1.0, reaperAddress : str = ReaperAPI.ADDRESS, reaperPath : str = None, projectPath : str = None, parent=None):
        super().__init__(parent)
        self.track = 0
        self.region = None
        self.reaperAddress = reaperAddress if reaperAddress else ReaperAPI.ADDRESS
        self.volume = volume
        self.reaper = None
        self.reaperPath = reaperPath
        self.projectPath = projectPath
        self.REAPER_DELAY = 0.2  # time delay for reaper connection
        self.REAPER_INIT_TIMEOUT = 20.0   # time to wait for reaper to initialize

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.finished.emit)

    def initReaper(self) -> bool:
        """ Initializes the player, must be called before playing any sample """
        logger.info("Initializing the player...")
        if not self.reaperPath:
            logger.warning("Reaper path not provided, Reaper will not be launched, make sure to launch it manually")
        else:
            if not self.projectPath:
                logger.warning("Reaper project path not provided, Reaper will be launched without a project, make sure, that the correct project is opened")
            logger.info("Starting the Reaper software...")
            launchReaper(self.reaperPath, self.reaperAddress, self.projectPath, self.REAPER_INIT_TIMEOUT)

        try:
            self.reaper = ReaperAPI(self.reaperAddress)
            self.reaper.command(
                self.reaper.Stop,
                self.reaper.Go_to_beginning,
                self.reaper.Unmute_all,
                self.reaper.Unsolo_all
            )
        except ReaperError as e:
            logger.error(f"Reaper connection not working: {e}")
            self.reaperError.emit()
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
            self.reaperError.emit()
            return False

        self.timer.start(int((region.duration + self.REAPER_DELAY) * 1000))
        logger.debug(f'Playing track {track} {"at region " + str(region) if region else ""}...')
        return True

    def playSample(self, sample : Sample) -> bool:
        if sample is None:
            logger.error("Failed to play, no sample provided")
            return False
        logger.debug(f'Playing sample "{sample.id if sample.id else ""}"...')
        return self.playTrack(sample.track, sample.region)

    def stop(self) -> bool:
        if self.reaper is None:
            logger.error("Player not initialized, call initReaper() first")
            return False
        try:
            self.reaper.command(self.reaper.Stop)
        except ReaperError as e:
            logger.error(f"Failed to stop playback: {e}")
            self.reaperError.emit()
            return False
        self.timer.stop()
        logger.debug("Playback stopped")
        return True

    def playing(self) -> bool:
        if self.reaper is None:
            logger.debug("Player not initialized, checking playing state is irrelevant")
            return False
        return self.timer.isActive()

    def setVolume(self, volume : float) -> bool:
        try:
            SystemVolume.SetVolume(level=volume, mute=False)
            self.volume = volume
        except Exception as e:
            logger.warning(f"Failed to set system volume to {volume}: {e}")
            return False
        logger.info(f"Set volume to {self.volume}")
        return True
