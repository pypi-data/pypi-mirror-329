from yta_general_utils.programming.validator import PythonValidator

import numpy as np


# TODO: Maybe I should move this class because
# it is more strictly related to moviepy audio
class AudioFrameEditor:
    """
    Class to simplify and encapsulate all the functionality
    related to audio frame edition (audio frame is a numpy).
    """

    @staticmethod
    def modify_volume(audio_frame: np.ndarray, factor: int = 100):
        return change_audio_volume(audio_frame, factor)
    
def change_audio_volume(audio_frame: np.ndarray, factor: int = 100):
    """
    Change the 'audio_frame' volume by applying the
    given 'factor'.

    Based on:
    https://github.com/Zulko/moviepy/blob/master/moviepy/audio/fx/MultiplyVolume.py
    """
    if not PythonValidator.is_numpy_array(audio_frame):
        raise Exception('The provided "audio" is not a numpy array.')
    
    number_of_channels = len(list(audio_frame[0]))
    factors_array = np.array([factor for _ in range(audio_frame.shape[0])])

    if number_of_channels == 1: return np.multiply(audio_frame, factors_array)
    if number_of_channels == 2:
        return np.multiply(
            audio_frame,
            np.array([factors_array for _ in range(number_of_channels)]).T,
        )