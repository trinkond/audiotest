### Written by Tomas Dudacek in project /mushra_py_ctu
### Edited by Ondrej Trinkewitz
### Creates a Regions object to store and access regions in Reaper

import os.path
import logging
logger = logging.getLogger(__name__)

class Region:
    """ data class containing Region data """

    def __init__(self, start_time : float, duration : float):
        self.start_time = start_time
        self.duration = duration

    def __repr__(self):
        return f"Region(start_time={self.start_time!r}, duration={self.duration!r})"

    def __str__(self):
        return repr(self)

    def toList(self):
        """ returns the Region data as list for easier saving """
        return [self.start_time, self.duration]

    @staticmethod
    def fromList(data : list):
        """ restores Region from list """
        try:
            return Region(float(data[0]), float(data[1]))
        except:
            logger.error(f"Wrong region list format {data}")
            return None

class Sample:
    """ data class containing Sample data """

    def __init__(self, track : int, region : Region):
        self.track = track
        self.region = region

    def __repr__(self):
        return f"Sample(track={self.track!r}, region={self.region!r})"

    def __str__(self):
        return repr(self)

class RegionReader:
    def __init__(filename : str):
        self.fname = filename

    def check_fname_format(self) -> bool:
        """ checks whether filename contains .csv """
        return self.fname.split('.')[-1] == "csv"

    def check_file_path(self) -> bool:
        """ checks whether given file exists """
        return os.path.isfile(self.fname)

    @staticmethod
    def parse_time(time : str) -> float:
        """ convert from h:mm:ss.fff to seconds """
        split_time = time.split(':')
        try:
            if len(split_time) == 1:
                minutes = 0
                seconds = float(split_time[0].strip())
            elif len(split_time) == 2:
                minutes = int(split_time[0].strip())
                seconds = float(split_time[1].strip())
            elif len(split_time) == 3:
                minutes = 24*int(split_time[0].strip()) + int(split_time[1].strip())
                seconds = float(split_time[2].strip())
            else:
                raise Exception(f"Unexpected number of fields {len(split_time)}")
            if len(split_time) > 1 and seconds > 60:
                raise Exception(f"Illegal time format with too many seconds ({seconds})")
        except:
            raise ValueError("Unsupported time format")
        
        return 60 * minutes + seconds

    def read_config(self) -> list[Region]:
        """ reads through given .csv file and returns a dict of Regions """
        logger.info(f'Loading regions from "{self.fname}"')

        if not self.check_fname_format():
            logger.warning(f'Unexpected region file extension "{self.fname}", expecting .csv')

        if not self.check_file_path():
            logger.error(f'File "{self.fname}" not found')
            return regions

        reg_count = 0
        regions = {}

        with open(self.fname, 'r') as f:
            for line in f:
                split_line = line.split(',')
                entry_code = split_line[0]

                if entry_code[0] == '#':            # comment line -> ignore
                    continue
                if entry_code[0] in ['M', 'm']:     # marker -> ignore
                    continue
                if entry_code[0] in ['R', 'r']:     # region
                    reg_id = entry_code[1:]
                else:
                    logger.error(f"Unsupported entry code {entry_code[0]}")
                    continue

                try:
                    reg_id = int(reg_id.strip())
                    t_s = self.parse_time(split_line[2])
                    t_d = self.parse_time(split_line[4])
                except:
                    logger.error(f'Unsupported region format "{line.strip()}"')
                    continue
                
                regions[reg_id] = Region(t_s, t_d)
                reg_count += 1

        if reg_count < 1:
            logger.warning("No regions were loaded, file is empty or there was a parsing error")
        else:
            logger.info(f"Successfully loaded {len(regions)} regions")
        return regions

