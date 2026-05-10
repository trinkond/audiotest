# Inspired by Tomas Dudacek in project /mushra_py_ctu
# Written by Ondrej Trinkewitz

import requests

class ReaperError(Exception):
    pass

class ReaperAPI:
    """ Class implementing communication with REAPER DAW over http """

    ADDRESS = "127.0.0.1:8080"

    @staticmethod
    def ping_server(address : str) -> bool:
        """ Checks if the Reaper server is reachable at the given address """
        try:
            resp = requests.get(address)
            return resp.ok
        except Exception as e:
            return False

    def __init__(self, address : str = ADDRESS):
        self.base_add = "http://" + address + "/_/"
        self.check_server()
        self.n_tracks = self.get_n_tracks()

    def check_server(self):
        try:
            resp = requests.get(self.base_add)
        except Exception as e:
            raise ReaperError(f"Server at address {self.base_add} not reached") from e
        if not resp.ok:
            raise ReaperError(f"Server not ok, responded with code {resp.status_code}")

    def get_n_tracks(self) -> int:
        try:
            resp = requests.get(self.base_add + 'NTRACK')
        except Exception as e:
            raise ReaperError(f"Failed to fetch number of tracks, server not reached") from e
        if not resp.ok:
            raise ReaperError(f"Failed to fetch number of tracks, server responded with code {resp.status_code}")
        try:
            n = int(resp.text.split('\t')[1].strip('\n'))
        except (IndexError, ValueError) as e:
            raise ReaperError(f'Failed to get the number of tracks from server message "{resp.text}"') from e
        if n < 0:
            raise ReaperError(f'Failed to get the number of tracks, {n} is invalid')
        return n 

    def command(self, *commands):
        """ Sends one or multiple commands to Reaper. Commands are strings separated with ';'. """
        try:
            resp = requests.get(self.base_add + ';'.join(commands))
        except Exception as e:
            raise ReaperError(f'Failed to send commands "{commands}", server not reached') from e
        if not resp.ok:
            raise ReaperError(f'Failed to send commands "{commands}", server responded with code {resp.status_code}')

    """ Basic commands """
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
