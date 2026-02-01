# Written by Tomas Dudacek in project /mushra_py_ctu

import requests
import logging
logger = logging.getLogger(__name__)

class Player:
    """ Class implementing communication with REAPER DAW """

    def __init__(self):
        self.BASE_ADD = 'http://127.0.0.1:8080/_/'
        
        if not self.check_server():
            logger.error("REAPER does not respond to call!")
            raise
        
        self.n_tracks = self.set_n_tracks()
        self.go_to_begining()
        self.unsolo_all()

    def check_server(self) -> bool:
        return requests.get(self.BASE_ADD).ok

    def set_n_tracks(self) -> int:
        resp = requests.get(self.BASE_ADD + 'NTRACK')
        print(resp.text)
        return int(resp.text.split('\t')[1].strip('\n'))

    def go_to_begining(self) -> None:
        requests.get(self.BASE_ADD + 'SET/POS/0')

    def go_to_time(self, time : float) -> None:
        requests.get(self.BASE_ADD + 'SET/POS/' + str(time))

    def solo_track(self,track_n : int) -> None:
        requests.get(self.BASE_ADD + 'SET/TRACK/'+str(track_n)+'/SOLO/1')

    def unsolo_track(self,track_n : int) -> None:
        requests.get(self.BASE_ADD + 'SET/TRACK/'+str(track_n)+'/SOLO/0')

    def play(self) -> None:
        requests.get(self.BASE_ADD + '1007')

    def next_frame(self) -> None:
        requests.get(self.BASE_ADD + '40173')

    def prev_frame(self) -> None:
        requests.get(self.BASE_ADD + '40172')

    def unsolo_all(self) -> None:
        for i in range(self.n_tracks):
            self.unsolo_track(i)

