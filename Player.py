# Written by Tomas Dudacek in project /mushra_py_ctu
# import logging
# logger = logging.getLogger(__name__)


import requests

class ReaperError(RuntimeError):
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
    """ Audio player interface for playing tracks through Reaper """

    def __init__(self):

        self.reaper = None
       


    
    def __enter__(self):
        self.reaper = ReaperAPI()
        self.n_tracks = self.reaper.n_tracks
        self.reaper.command(
            self.Stop,
            self.Go_to_beginning,
            self.Unmute_all,
            self.Unsolo_all,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def play(self):
        pass


    def stop(self):
        pass






if __name__ == "__main__":
    player = Player()



## Chat generated example to unmute only Reaper
    from audiomath.SystemVolume import SystemVolumeSetting, MAX_VOLUME

    # Your desired master volume (0.0–1.0)
    DESIRED_VOLUME = 0.5

    # Step 1: Set master volume
    MASTER_VOL = SystemVolumeSetting(level=DESIRED_VOLUME, mute=False)

    # Step 2: Mute all sessions (except Reaper)
    MUTE_ALL = SystemVolumeSetting(mute=True, session=None)  # session=None mutes all apps

    # Step 3: Unmute Reaper
    REAPER_UNMUTE = SystemVolumeSetting(mute=False, session="Reaper")

    # Combine settings: master volume + mute all + unmute Reaper
    with MASTER_VOL & MUTE_ALL & REAPER_UNMUTE:
        print("Volume set. Everything muted except Reaper.")
        input("Press Enter to restore original system settings...")
