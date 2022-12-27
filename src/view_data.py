import librosa
import soundfile as sf

SR = [
    11025,
    16000,
    22050,
    32000,
    44100,
    48000,
    96000
]

FORMAT = sf.available_formats().keys()
SUBTYPE = sf.available_subtypes().keys()
