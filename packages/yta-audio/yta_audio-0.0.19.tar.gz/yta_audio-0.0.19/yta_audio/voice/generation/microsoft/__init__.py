from yta_audio.voice.enums import NarrationLanguage
from yta_audio.voice.generation.voices import NarrationVoice
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from typing import Union

import pyttsx3


class MicrosoftVoiceName(Enum):
    """
    Available voices. The value is what is used
    for the audio creation.
    """

    SPANISH_SPAIN = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
    SPANISH_MEXICO = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
    # TODO: There are more voices

VOICE_NAME_OPTIONS = MicrosoftVoiceName.get_all()
LANGUAGE_OPTIONS = [
    NarrationLanguage.DEFAULT
]

class MicrosoftNarrationVoice(NarrationVoice):
    """
    Voice instance to be used when narrating with
    Microsoft engine.
    """

    def validate_and_process(
        self,
        name: str,
        emotion: str,
        speed: float,
        pitch: float,
        language: NarrationLanguage
    ):
        super().validate_and_process(name, emotion, speed, pitch, language)

        MicrosoftVoiceName.to_enum(name)

        # Speed must be a value similar to 130

        return name, emotion, speed, pitch, language
        
    @staticmethod
    def default():
        return MicrosoftNarrationVoice(MicrosoftVoiceName.SPANISH_SPAIN.value, '', 130, 1.0, NarrationLanguage.DEFAULT)

def narrate(
    text: str,
    voice: MicrosoftNarrationVoice = MicrosoftNarrationVoice.default(),
    output_filename: Union[str, None] = None
):
    """
    Creates an audio narration of the provided 'text'
    and stores it as 'output_filename'.
    """
    output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
    
    # TODO: This is hardcoded, be careful!
    engine = pyttsx3.init()
    #engine = pyttsx3.init()
    engine.setProperty('voice', voice.name)
    # Default speed is 200 (wpm)
    engine.setProperty('rate', int(voice.speed))
    engine.save_to_file(text, output_filename)
    engine.runAndWait()

    return output_filename