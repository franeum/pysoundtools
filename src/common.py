#!/usr/bin/env python3

"""common data"""

import sox

DEFDROP = '---'
SR = [
    DEFDROP,
    11025,
    16000,
    22050,
    32000,
    44100,
    48000,
    96000
]
CHANNELS = [DEFDROP, 'Mono', 'Stereo', 3, 4, 5, 6, 7, 8]
FORMATS = None


def extract_file_formats():
    global FORMATS
    data = sox.core.sox(['-h'])[1]
    splitted = data.splitlines()
    formats = [x for x in splitted if "AUDIO FILE FORMATS" in x][0]
    formats = formats.partition('AUDIO FILE FORMATS: ')[2]
    FORMATS = [DEFDROP] + formats.split(' ')
    return None


extract_file_formats()
