from yta_audio.voice.enums import NarrationLanguage
from yta_audio.voice.generation.voices import NarrationVoice
from yta_general_utils.downloader import Downloader
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union

import requests


"""
These below are the options of voice name
and language. These options are here to 
make it customizable. If there is only
once choice, or no choice, the options
array will have a None element.

These options will be used to be selected
when provided as an API service.
"""
class Ttsmp3VoiceName(Enum):
    LUPE = 'Lupe'
    PENELOPE = 'Penelope'
    MIGUEL = 'Miguel'

VOICE_NAME_OPTIONS = Ttsmp3VoiceName.get_all()
LANGUAGE_OPTIONS = [
    NarrationLanguage.DEFAULT
]

class Ttsmp3NarrationVoice(NarrationVoice):
    """
    Voice instance to be used when narrating with
    Ttsmp3 engine.
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

        Ttsmp3VoiceName.to_enum(name)
        
        return name, emotion, speed, pitch, language
        
    @staticmethod
    def default():
        return Ttsmp3NarrationVoice(Ttsmp3VoiceName.LUPE.value, '', 1.0, 1.0, NarrationLanguage.DEFAULT)

# TODO: Check this because I don't know if this webpage is using the tts (coqui)
# library as the generator engine. If that, I have this engine in 'coqui.py' file
# so I don't need this (that is not stable because is based in http requests)
def narrate_tts3(
    text: str,
    voice: Ttsmp3NarrationVoice = Ttsmp3NarrationVoice.default(),
    output_filename: Union[str, None] = None
) -> str:
    """
    This makes a narration based on an external platform. You
    can change some voice configuration in code to make the
    voice different.

    Aparrently not limited. Check, because it has time breaks 
    and that stuff to enhance the narration.
    """
    # From here: https://ttsmp3.com/
    headers = {
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://ttsmp3.com',
        'referer': 'https://ttsmp3.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    data = {
        'msg': text,
        'lang': voice.name,
        'source': 'ttsmp3',
    }

    response = requests.post('https://ttsmp3.com/makemp3_new.php', headers = headers, data = data)
    response = response.json()
    url = response['URL']

    output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)

    # "https://ttsmp3.com/created_mp3/8b38a5f2d4664e98c9757eb6db93b914.mp3"
    Downloader.download_audio(url, output_filename)

    return output_filename