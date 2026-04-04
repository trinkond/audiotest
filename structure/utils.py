""" Utility functions for the audio test application """

import logging
logger = logging.getLogger(__name__)

def loadDefault(data : dict, default : dict) -> dict:
    """ Loads data from the dict, filling missing keys with defaults and checking type """
    data = data.copy()
    for key in default:
        if not key in data:
            logger.warning(f'Missing entry for "{key}", filled with default value {default[key]}')
            data[key] = default[key]
            continue
        if default[key] is None:
            continue
        if type(data[key]) != type(default[key]):
            logger.error(f'Entry for "{key}" is incompatible format {type(data[key])}, default value {default[key]} has been taken')
            data[key] = default[key]
    return data


