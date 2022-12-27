"""AudioConverter class"""

from pathlib import Path
import sox
import common

MOCKINPUT = '/home/neum/Documenti/jeff/DATABASE_JF/AUDIO_FILES/Bol_01.mp3'
MOCKOUTPUT = '/home/neum/Documenti/audio_converter/stokazzo.aif'


class AudioConverter:
    """wrapper for sox Transformer"""

    def __init__(self):
        self.tfm = sox.Transformer()

    @property
    def sourcepath(self):
        """get source file path"""
        return self._sourcepath

    @sourcepath.setter
    def sourcepath(self, value):
        """set source file path"""
        self._sourcepath = Path(value)

    @property
    def destpath(self):
        """get destination file path"""
        return self._destpath

    @destpath.setter
    def destpath(self, value):
        """set destination file path"""
        self._destpath = Path(value)

    @property
    def samplerate(self):
        """get samplerate"""
        return self._samplerate

    def set_samplerate(self, value):
        """set samplerate"""
        self.tfm.rate(value, 'v')
        self._samplerate = int(value)

    @property
    def channels(self):
        """get n of channels"""
        return self._channels

    # setter
    def set_channels(self, value):
        self.tfm.channels(common.CHANNELS.index(value))
        self._channels = common.CHANNELS.index(value)

    @property
    def audioformat(self):
        """get format"""
        return self._format

    def set_format(self, value):
        """set format"""
        self.tfm.set_output_format(file_type=value)
        self._format = value

    def export(self):
        """export audio to file"""
        # self.tfm.build_file(self._sourcepath, self._destpath)
        print(self.tfm.__dict__)
        self.tfm.build_file(MOCKINPUT, MOCKOUTPUT)
