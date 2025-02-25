from yta_audio.voice.enums import NarrationLanguage
from yta_audio.voice.generation.voices import NarrationVoice
from yta_general_utils.file.writer import FileWriter
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from typing import Union

import requests


class TetyysVoiceName(Enum):
    """
    Available voices. The value is what is used
    for the audio creation.
    """

    SAM = 'sam'
    # TODO: There are more voices

VOICE_NAME_OPTIONS = TetyysVoiceName.get_all()
LANGUAGE_OPTIONS = [
    NarrationLanguage.DEFAULT
]

class TetyysNarrationVoice(NarrationVoice):
    """
    Voice instance to be used when narrating with
    Tiktok engine.
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

        TetyysVoiceName.to_enum(name)

        # TODO: Maybe force speed and pitch values in a
        # decent range (from 80 to 160 or similar)

        return name, emotion, speed, pitch, language
        
    @staticmethod
    def default():
        return TetyysNarrationVoice(TetyysVoiceName.SAM.value, '', 100, 150, NarrationLanguage.DEFAULT)

def narrate_tetyys(
    text: str,
    voice: TetyysNarrationVoice = TetyysNarrationVoice.default(),
    output_filename: Union[str, None] = None
):
    """
    This method creates an audio voice narration of the provided
    'text' read with tthe tetyys system voice (Microsoft Speech
    API 4.0 from 1998) and stores it as 'output_filename'. It is 
    only available for ENGLISH speaking.

    You can change some voice parameters in code to make it a
    different voice.

    This method is requesting an external (but apparently stable
    website).
    """
    # This was taken from here (https://www.tetyys.com/SAPI4/)
    if not text:
        return None
    
    headers = {
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://www.tetyys.com/SAPI4/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    params = {
        'text': text,
        # Inspect options 'value' from https://www.tetyys.com/SAPI4/ but
        # each voice has a pre-set 'pitch' and 'speed' 
        'voice': voice.name, 
        'pitch': str(int(voice.pitch)),
        'speed': str(int(voice.speed)),
    }

    """
    Some VOICE options:
        'Male Whisper' 113, 140
        'Female Whisper' 169, 140
        'Mary' 169, 140
        'Mary in Space'|'Mary in Hall'|'Mary in Stadium'|Mary (for Telephone) 169, 140
        'Mike in Space'|... 113, 140
        'RobosoftOne'|'RobosoftTwo'
        'Sam' 100, 140
    """

    output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)

    response = requests.get('https://www.tetyys.com/SAPI4/SAPI4', params = params, headers = headers)

    FileWriter.write_binary_file(response.content, output_filename)

    return output_filename