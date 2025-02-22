from yta_audio.converter import AudioConverter
from moviepy import AudioClip
from pydub import AudioSegment
from typing import Union

import numpy as np


class AudioParser:
    """
    Class to simplify the way we parse audios.
    """

    @staticmethod
    def as_audioclip(
        audio: Union[str, np.ndarray, AudioSegment, AudioClip]
    ):
        audio, _ = AudioConverter.to_audioclip(audio)

        return audio
    
    @staticmethod
    def as_audiosegment(
        audio: Union[str, np.ndarray, AudioSegment, AudioClip]
    ):
        audio, _ = AudioConverter.to_audiosegment(audio)

        return audio
    
    # TODO: '.as_numpy()' ? It is difficult due to rate
    # or strange mapping... (?)