# Written by Tomas Dudacek in project /mushra_py_ctu
# import logging
# logger = logging.getLogger(__name__)


import requests

class ReaperError(RuntimeError):
    pass

class Player:
    """ Class implementing communication with REAPER DAW over http """

    def __init__(self):
        self.BASE_ADD = "http://127.0.0.1:8080/_/"
        
        self.check_server()
        self.n_tracks = self.get_n_tracks()
        self.command(
            self.Stop,
            self.Go_to_beginning,
            self.Unmute_all,
            self.Unsolo_all,
        )

    def check_server(self):
        try:
            resp = requests.get(self.BASE_ADD)
        except:
            raise ReaperError("Failed to check the server!")
        if not resp.ok:
            raise ReaperError(f"Server not ok, responded with code {resp.status_code}")

    def get_n_tracks(self) -> int:
        try:
            resp = requests.get(self.BASE_ADD + 'NTRACK')
        except:
            raise ReaperError("Failed to fetch the number of tracks!")
        if not resp.ok:
            return None
        return int(resp.text.split('\t')[1].strip('\n'))

    def command(self, *commands):
        """ Sends one or multiple commands to Reaper. Commands are strings separated with ';'. """
        try:
            resp = requests.get(self.BASE_ADD + ';'.join(commands))
        except:
            raise ReaperError(f'Failed to send commands "{commands}"!')
        return resp.ok

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

if __name__ == "__main__":
    player = Player()

