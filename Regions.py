### Written by Tomas Dudacek in project /mushra_py_ctu
### Edited by Ondrej Trinkewitz
### Creates a Regions object to store and access regions in Reaper

import os.path
import logging
logger = logging.getLogger(__name__)

class Region:
    """ data class containing Region data"""

    def __init__(self, start_time : float, duration : float):
        self.start_time = start_time
        self.duration = duration

    def __repr__(self):
        return f"Region(start_time={self.start_time!r}, duration={self.duration!r})"

        
    def __str__(self):
        return repr(self)

class RegionReader():
    """ 
        Class for reading region info from generated .csv file
        NOTE: could be a subclass of abstract class Reader - but... python...
    """

    def __init__(self, fname : str, n_frames : int):
        self.n_frames : int = n_frames
        self.fname : str = fname
        self.regions : dict[Region] = {}

    def check_fname_format(self) -> bool:
        """ checks whether filename contains .csv """

        if self.fname.split('.')[1] != "csv":
            logger.error("Wrong file format!")
            return False

        return True

    def check_file_path(self) -> bool:
        """ checks whether given file exists """

        if not os.path.isfile(self.fname):
            logger.error("No such file exists!")
            return False

        return True

    def read_config(self) -> list[Region]:
        """ reads through given .csv file and returns a list of region start times """

        if not self.check_fname_format():
            return None

        if not self.check_file_path():
            return None

        cc : int = 0
        self.regions : list[Region] = {}

        with open(self.fname, 'r') as f:
            for line in f:
                split_line : list = line.split(',')
                
                entry_code = split_line[0]

                if entry_code[0] == '#':            # comment line -> ignore
                    continue
                if entry_code[0] in ['M', 'm']:     # marker -> ignore
                    continue
                if entry_code[0] in ['R', 'r']:     # region
                    reg_id = entry_code[1:]
                else:
                    logger.error(f"Unsupported entry code {entry_code}")
                    continue

                try:
                    reg_id = int(reg_id.strip())

                    # Start time
                    t_str : str = split_line[2]
                    t_s : float = float(t_str.split(':')[1])+float(t_str.split(':')[0]*60)

                    # Duration
                    t_str = split_line[4]
                    t_d = float(t_str.split(':')[1])+float(t_str.split(':')[0]*60)

                    self.regions[reg_id] = Region(t_s, t_d)

                except:
                    logger.error("Entry file format!")
                    return None

                cc+=1

    #    if cc != self.n_frames:
    #        logger.error("Invalid region number - file incoherence!")
    #        return None

        if cc < 1:
            logger.error("Config file is empty!")
            return None
        
        return self.regions

