"""AudioConverter class"""

from pathlib import Path
import sox

MOCKINPUT = Path(
    '/home/neum/Documenti/jeff/DATABASE_JF/AUDIO_FILES/Bol_01.mp3')
MOCKOUTPUT = Path('/home/neum/Documenti/pysoundtools/stokazzo.aif')


class AudioConverter:
    """wrapper for sox Transformer"""

    def __init__(self):
        self.tfm = sox.Transformer()
        self._format = None
        self._samplerate = None
        self._channels = None

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

    @samplerate.setter
    def samplerate(self, value):
        """set samplerate"""
        self.tfm.rate(value, 'v')
        self._samplerate = int(value)

    @property
    def channels(self):
        """get n of channels"""
        return self._channels

    @channels.setter
    def channels(self, value):
        "set nr of channels"
        self.tfm.channels(value)
        self._channels = value

    @property
    def audioformat(self):
        """get format"""
        return self._format

    @audioformat.setter
    def audioformat(self, value):
        """set format"""
        self.tfm.set_output_format(file_type=value)
        self._format = value

    def clear(self):
        self.tfm.clear_effects()

    def export(self):
        """export audio to file"""
        # self.tfm.build_file(self._sourcepath, self._destpath)
        print(self.tfm.__dict__)
        print(self.sourcepath, self.destpath)
        self.tfm.build_file(str(self.sourcepath), str(self.destpath))
