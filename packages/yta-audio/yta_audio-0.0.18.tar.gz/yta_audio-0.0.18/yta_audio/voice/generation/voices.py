"""
# TODO: Rename this file I think
"""
from yta_audio.voice.enums import NarrationLanguage
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.validator.number import NumberValidator
from dataclasses import dataclass
from abc import abstractmethod


@dataclass
class NarrationVoice:
    """
    Dataclass to be implemented by other custom
    dataclasses that will determine the narration
    voice parameters of our voice narration 
    engines.
    """

    name: str
    """
    The voice narration name.
    """
    emotion: str
    """
    The voice narration emotion.
    """
    speed: float
    """
    The voice narration desired speed.
    """
    pitch : float
    """
    The voice narration desired pitch.
    """
    language: NarrationLanguage
    """
    The language to be used with the voice narration.
    """
    # TODO: Maybe add something more like
    # pitch or something

    def __init__(
        self,
        name: str = '',
        emotion: str = '',
        speed: float = 1.0,
        pitch: float = 1.0,
        language: NarrationLanguage = NarrationLanguage.DEFAULT
    ):
        name, emotion, speed, pitch, language = self.validate_and_process(name, emotion, speed, pitch, language)

        self.name = name
        self.emotion = emotion
        self.speed = speed
        self.pitch = pitch
        self.language = language

    @abstractmethod
    def validate_and_process(
        self,
        name: str,
        emotion: str,
        speed: float,
        pitch: float,
        language: NarrationLanguage
    ):
        """
        Check if the parameters provided are valid or not
        and raise an Exception if not.

        This method can also process the attributes to make
        some modifications and return them to be stored
        once they have been modified.

        This method must be overwritten.
        """
        if not PythonValidator.is_string(name):
            raise Exception('The provided "name" parameter is not a string.')
        
        if not PythonValidator.is_string(emotion):
            raise Exception('The provided "emotion" parameter is not a string.')
        
        if not NumberValidator.is_positive_number(speed):
            raise Exception('The provided "speed" parameter is not a positive number.')
        
        if not NumberValidator.is_positive_number(pitch):
            raise Exception('The provided "pitch" parameter is not a positive number.')
        
        NarrationLanguage.to_enum(language)

        return name, emotion, speed, pitch, language

    @staticmethod
    @abstractmethod
    def default():
        """
        Return an instance of your Narration Voice custom
        class with the default values for that type of 
        class.

        This method must be overwritten.
        """
        pass

