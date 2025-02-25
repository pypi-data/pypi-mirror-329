from yta_audio.parser import AudioParser
from yta_general_utils.programming.validator.number import NumberValidator
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileExtension
from pydub import AudioSegment, silence
from typing import Union


class AudioSilence:
    """
    Class to simplify and encapsulate the interaction with
    audio silences.
    """

    @staticmethod
    def detect(
        audio,
        minimum_silence_ms: int = 250
    ):
        """
        Detect the silences of a minimum of 'minimum_silence_ms'
        milliseconds time and returns an array containing tuples
        with the start and the end of the silence moments.

        This method returns an array of tuples with the start 
        and the end of each silence expressed in seconds.
        """
        audio = AudioParser.as_audiosegment(audio)

        minimum_silence_ms = 250 if not minimum_silence_ms else minimum_silence_ms

        if not NumberValidator.is_positive_number(minimum_silence_ms):
            raise Exception('The provided "minimum_silence_ms" is not a positive number.')

        dBFS = audio.dBFS
        # TODO: Why '- 16' (?) I don't know
        silences = silence.detect_silence(audio, min_silence_len = minimum_silence_ms, silence_thresh = dBFS - 16)

        # [(1.531, 1.946), (..., ...), ...] in seconds
        return [
            ((start / 1000), (stop / 1000))
            for start, stop in silences
        ]
    
    @staticmethod
    def create(
        duration: float,
        frame_rate: int = 11025,
        output_filename: Union[str, None] = None
    ):
        """
        Create a silence audio of the given 'duration'. The
        frame rate could be necessary due to different
        videos frame rates.
        
        The file will be stored locally only if
        'output_filename' parameter is provided.
        """
        if not NumberValidator.is_positive_number(duration, do_include_zero = False):
            raise Exception('The provided "duration" is not a positive number.')
        
        # This is the default value for AudioSegment
        frame_rate = 11025 if frame_rate is None else frame_rate

        silence = AudioSegment.silent(duration * 1000, frame_rate)

        """
        if 'output_filename' is True => '.Temp.create_filename()'
        if 'output_filename' is str => validate extension and/or fix it with '.Temp.create_filename()'
        if 'output_filename' is anything else => NOT STORED
        """

        if output_filename is not None:
            # TODO: Validate output and extension
            silence.export(Output.get_filename(output_filename, FileExtension.MP3), format = 'mp3')

        # TODO: Maybe return a FileReturn (?)
        return AudioParser.as_audioclip(silence)
    
__all__ = [
    'AudioSilence'
]