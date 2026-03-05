### Written by Tomas Dudacek in project /mushra_py_ctu
### Edited by Ondrej Trinkewitz
### Creates a Regions object to store and access regions in Reaper

import os.path
import logging
logger = logging.getLogger(__name__)

class Region:
    """ data class containing Region data """

    def __init__(self, start_time : float, duration : float, id : int = None):
        self.id : int = id
        self.start_time : float = start_time
        self.duration : float = duration

    def __repr__(self):
        id = "" if self.id is None else str(self.id)
        return f"Region{id}(start_time={self.start_time!r}, duration={self.duration!r})"

    def __str__(self):
        return repr(self)

    def toList(self):
        """ returns the Region data as list for easier saving """
        return [self.start_time, self.duration]

    @staticmethod
    def fromList(data : list, id : int = None):
        """ restores Region from list """
        try:
            return Region(float(data[0]), float(data[1]), int(id))
        except (IndexError, TypeError, ValueError):
            logger.error(f"Wrong region list format {data}")
            return None

class Sample:
    """ data class containing Sample data """

    def __init__(self, track : int, region : Region, id : str = None):
        self.id : str = id
        self.track : int = track
        self.region : Region = region

    def __repr__(self):
        id = "" if self.id is None else f'"{str(self.id)}"' 
        return f"Sample{id}(track={self.track!r}, region={self.region!r})"

    def __str__(self):
        return repr(self)

def check_fname_csv(fname : str) -> bool:
    """ checks whether filename contains .csv """
    return fname.split('.')[-1] == "csv"

def check_file_path(fname : str) -> bool:
    """ checks whether given file exists """
    return os.path.isfile(fname)

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

def read_config(fname : str) -> dict[int, Region]:
    """ reads through given .csv export from Reaper and returns a dict of Regions """
    logger.info(f'Loading regions from "{fname}"')

    if not check_fname_csv(fname):
        logger.warning(f'Unexpected region file extension "{fname}", expecting .csv')

    if not check_file_path(fname):
        logger.error(f'File "{fname}" not found')
        return {}

    reg_count = 0
    regions = {}

    with open(fname, 'r') as f:
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
                t_s = parse_time(split_line[2])
                t_d = parse_time(split_line[4])
            except (IndexError, TypeError, ValueError):
                logger.error(f'Unsupported region format "{line.strip()}"')
                continue
            
            regions[reg_id] = Region(t_s, t_d, reg_id)
            reg_count += 1

    if reg_count < 1:
        logger.warning("No regions were loaded, file is empty or there was a parsing error")
    else:
        logger.info(f"Successfully loaded {len(regions)} regions")
    return regions

def validateRegions(regs : dict[int, Region]) -> bool:
    """ tests whether a given dict of regions is valid for playback """
    valid = True
    for key, val in regs.items():
        if type(key) != int or not isinstance(val, Region):
            logger.warning(f"Region {key} not valid, found {val}")
            valid = False
            continue
        if val.id != key:
            logger.warning(f"Region {val.id} is found at a key {key} not matching its id")
            valid = False
    return valid

def validateSamples(samples : dict[str, Sample], n_tracks : int = None) -> bool:
    """ tests whether a given dict of samples is valid for playback """
    valid = True
    for id, val in samples.items():
        if type(id) != str or not isinstance(val, Sample):
            logger.warning(f'Sample "{id}" not valid, found {val}')
            valid = False
            continue
        if not isinstance(val.region, Region):
            logger.warning(f'Sample "{id}", contains invalid region {val.region}')
            valid = False
            continue
        if type(val.track) != int or (type(n_tracks) == int and not val.track in range(1, n_tracks+1)):
            logger.warning(f'Sample "{id}", contains invalid track number {val.track}')
            valid = False
            continue
        if val.id != id:
            logger.warning(f"Sample {val.id} is found at key {id} not matching its id")
            valid = False
    return valid

def parseRegions(data : dict) -> dict[int, Region]:
    """ reads the json formatted regions entry into Region objects
    invalid regions are parsed as None """
    logger.info(f"Parsing regions")
    regions = {}
    cc = 0
    for reg, dat in data.items():
        try:
            reg = int(reg)
        except (ValueError, TypeError):
            logger.error(f'Unsupported region ID "{reg}"')
            continue

        dat = Region.fromList(dat, reg)
        if dat is None:
            logger.error(f"Failed to parse region {reg}")
        else:
            cc += 1
        regions[reg] = dat

    if regions == {}:
        logger.warning("No regions were parsed")
    else:
        logger.info(f"Successfully parsed {cc} regions")
    return regions

def saveRegions(regions : dict[int, Region]) -> dict:
    """ formats the Regions as a dict for saving as json """
    data = {}
    for reg in regions.values():
        data[str(reg.id)] = reg.toList()
    return data

def parseSamples(data : dict, regions: dict[int, Region]) -> dict[str, Sample]:
    """ reads the json formatted samples entry into Sample objects
    matches and adds the corresponding regions, if not found, puts None """
    logger.info(f"Parsing samples")
    samples = {}
    cc = 0
    for id, dat in data.items():
        id = str(id)
        try:
            if type(dat) != list or len(dat) != 2:
                raise TypeError()
            track = int(dat[0])
            regid = int(dat[1])
        except (TypeError, ValueError, IndexError):
            logger.error(f'Sample "{id}" is in incompatible format')
            samples[id] = None
            continue
        try:
            region = regions[regid]
            cc += 1
        except KeyError:
            logger.warning(f'Region {regid} needed by sample "{id}" not found')
            region = None

        samples[id] = Sample(track, region, id)

    if samples == {}:
        logger.warning("No samples were parsed")
    else:
        logger.info(f"Successfully parsed {cc} samples")
    return samples

def saveSamples(samples : dict[str, Sample]) -> dict:
    """ formats the Samples as a dict for saving as json """
    data = {}
    for sample in samples.values():
        data[str(sample.id)] = [int(sample.track), int(sample.region.id)]
    return data
