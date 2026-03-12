# Inspired by Tomas Dudacek in project /mushra_py_ctu
# Written by Ondrej Trinkewitz

import requests
import time
import logging
from audiomath import SystemVolume
from Samples import Region, Sample

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReaperError(RuntimeError):
    pass

class PlaybackError(Exception):
    pass

class ReaperAPI:
    """ Class implementing communication with REAPER DAW over http """

    def __init__(self):
        self.BASE_ADD = "http://127.0.0.1:8080/_/"
        self.check_server()
        self.n_tracks = self.get_n_tracks()

    def check_server(self):
        resp = requests.get(self.BASE_ADD)
        if not resp.ok:
            raise ReaperError(f"Server not ok, responded with code {resp.status_code}")

    def get_n_tracks(self) -> int:
        resp = requests.get(self.BASE_ADD + 'NTRACK')
        if not resp.ok:
            raise ReaperError(f"Failed to fetch number of tracks, server responded with code {resp.status_code}")
        try:
            n = int(resp.text.split('\t')[1].strip('\n'))
        except (IndexError, ValueError) as e:
            raise ReaperError(f'Failed to fetch number of tracks, server message "{resp.text}"') from e
        if n < 0:
            raise ReaperError(f'Failed to fetch number of tracks, {n} is invalid')
        return n 

    def command(self, *commands):
        """ Sends one or multiple commands to Reaper. Commands are strings separated with ';'. """
        resp = requests.get(self.BASE_ADD + ';'.join(commands))
        if not resp.ok:
            raise ReaperError(f'Failed to send commands "{commands}", server responded with code {resp.status_code}')

    """" Basic commands """
    Go_to_beginning = "SET/POS/0"
    def Go_to_time(self, time): return f"SET/POS/{time}"

    def Solo_track(self, track): return f"SET/TRACK/{track}/SOLO/1"
    def Unsolo_track(self, track): return f"SET/TRACK/{track}/SOLO/0"
    def Solo_toggle(self, track): return f"SET/TRACK/{track}/SOLO/-1"
    @property
    def Solo_all(self): return ';'.join([self.Solo_track(i) for i in range(1, self.n_tracks+1)])
    @property
    def Unsolo_all(self): return ';'.join([self.Unsolo_track(i) for i in range(1, self.n_tracks+1)])

    def Mute_track(self, track): return f"SET/TRACK/{track}/MUTE/1"
    def Unmute_track(self, track): return f"SET/TRACK/{track}/MUTE/0"
    def Mute_toggle(self, track): return f"SET/TRACK/{track}/MUTE/-1"
    @property
    def Mute_all(self): return ';'.join([self.Mute_track(i) for i in range(1, self.n_tracks+1)])
    @property
    def Unmute_all(self): return ';'.join([self.Unmute_track(i) for i in range(1, self.n_tracks+1)])

    Play = "1007"
    Pause = "1008"
    Stop = "1016"

    Next_marker = "40173"
    Prev_marker = "40172"

class Player:
    """ Audio player interface for playing tracks using Reaper """

    def __init__(self, volume : float = 1.0):
        self.track = 0
        self.region = None
        self.playback_started = 0.0
        self.playback_stopped = False
        self.volume = volume
        self.REAPER_DELAY = 0.2  # safety time delay for reaper connection

        self.reaper = ReaperAPI()
        self.setVolume(self.volume)
        self.reaper.command(
            self.reaper.Stop,
            self.reaper.Go_to_beginning,
            self.reaper.Unmute_all,
            self.reaper.Unsolo_all,
        )

    def playTrack(self, track : int, region : Region):
        if not track in range(1, self.reaper.n_tracks+1):
            raise PlaybackError(f"There is no track with number {track}")
        self.setVolume(self.volume)
        self.reaper.command(
            self.reaper.Unmute_all,
            self.reaper.Unsolo_all,
            self.reaper.Solo_track(track),
            self.reaper.Go_to_time(region.start_time),
            self.reaper.Play,
            )
        self.playback_started = time.perf_counter()
        self.playback_stopped = False
        self.region = region
        self.track = track

    def playSample(self, sample : Sample):
        playTrack(sample.track, sample.region)

    def stop(self):
        self.reaper.command(self.reaper.Stop)
        self.playback_stopped = True

    def playing(self) -> bool:
        if self.playback_stopped:
            return False
        playback_end = self.playback_started + self.regions[self.region].duration
        playback_end += self.REAPER_DELAY
        if time.perf_counter() > playback_end:
            return False
        return True

    def setVolume(self, volume : float):
        self.volume = volume
        SystemVolume.SetVolume(level=self.volume, mute=False)

if __name__ == "__main__":
    from Samples import read_config
    regions = read_config(input("Enter region file name: "))
    player = Player()
    player.playTrack(2, regions[3])
    while(player.playing()):
        #print("p", end="")
        pass

