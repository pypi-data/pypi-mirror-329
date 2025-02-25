from yta_audio.voice.enums import NarrationLanguage
from yta_general_utils.text.transformer import remove_non_ascii_characters
from yta_audio.voice.generation.voices import NarrationVoice
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from typing import Union

import requests
import base64



class TiktokVoiceName(Enum):
    """
    Available voices. The value is what is used
    for the audio creation.
    """

    SPANISH = 'es_002'
    MEXICAN = 'es_mx_002'
    # TODO: There a a lot of English US and more languages voices

VOICE_NAME_OPTIONS = TiktokVoiceName.get_all()
LANGUAGE_OPTIONS = [
    NarrationLanguage.DEFAULT
]

class TiktokNarrationVoice(NarrationVoice):
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

        TiktokVoiceName.to_enum(name)

        return name, emotion, speed, pitch, language
        
    @staticmethod
    def default():
        return TiktokNarrationVoice(TiktokVoiceName.SPANISH.value, '', 1.0, 1.0, NarrationLanguage.DEFAULT)
    
def narrate_tiktok(
    text: str,
    voice: TiktokNarrationVoice = TiktokNarrationVoice.default(),
    output_filename: Union[str, None] = None
):
    """
    This is the tiktok voice based on a platform that generates it.
    This will make a narration with the tiktok voice. You can
    change the code to use the mexican voice.

    As this is based on an external platform, it could fail.
    """
    # From here: https://gesserit.co/tiktok    
    # A project to use Tiktok API and cookie (https://github.com/Steve0929/tiktok-tts)
    # A project to use Tiktok API and session id (https://github.com/oscie57/tiktok-voice)
    # A project that is install and play (I think) https://github.com/Giooorgiooo/TikTok-Voice-TTS/blob/main/tiktokvoice.py

    headers = {
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://gesserit.co',
        'referer': 'https://gesserit.co/tiktok',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    # Non-English characters are not accepted by Tiktok TTS generation, so:
    text = remove_non_ascii_characters(text)
    
    #data = f'{"text":"{text}","voice":"{voice.name}"}'
    data = '{"text":"' + text + '","voice":"' + voice.name + '"}'

    response = requests.post('https://gesserit.co/api/tiktok-tts', headers=headers, data=data)
    response = response.json()
    base64_content = response['base64']

    output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)

    try:
        content = base64.b64decode(base64_content)
        with open(output_filename,"wb") as f:
            f.write(content)
    except Exception as e:
        print(str(e))

    return output_filename
    