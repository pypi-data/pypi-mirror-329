from yta_audio.voice.enums import NarrationLanguage
from yta_audio.voice.generation.voices import NarrationVoice
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from typing import Union
from TTS.api import TTS

"""
These below are the options of voice name
and language. These options are here to 
make it customizable. If there is only
once choice, or no choice, the options
array will have a None element.

These options will be used to be selected
when provided as an API service.
"""
VOICE_NAME_OPTIONS = [
    None
]
LANGUAGE_OPTIONS = [
    NarrationLanguage.SPANISH,
    NarrationLanguage.DEFAULT
]

class TortoiseNarrationVoice(NarrationVoice):
    """
    Voice instance to be used when narrating with
    Tortoise engine.
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

        if language not in LANGUAGE_OPTIONS:
            raise Exception('The provided "language" is not a valid one.')
        
        # TODO: If more languages added,
        language = {
            NarrationLanguage.SPANISH: 'es',
            NarrationLanguage.DEFAULT: 'es'
        }[NarrationLanguage.to_enum(language)]

        return name, emotion, speed, pitch, language
        
    @staticmethod
    def default():
        return TortoiseNarrationVoice('', '', 1.0, 1.0, NarrationLanguage.DEFAULT)

def narrate(
    text: str,
    voice: TortoiseNarrationVoice = TortoiseNarrationVoice.default(),
    output_filename: Union[str, None] = None
):
    """
    @deprecated

    TODO: Remove this file and method if useless. Please, read below to check.
    This method should be removed and also the file as it is only one specific
    model in TTS narration library. It is not a different system. So please,
    remove it if it won't be used.
    """
    output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)

    # TODO: Delete tortoise lib?
    # TODO: Delete en/multi-datase/tortoise-v2 model
    tts = TTS("tts_models/es/multi-dataset/tortoise-v2")

    # Check code here: https://docs.coqui.ai/en/latest/models/tortoise.html
    tts.tts_to_file(text = text, language = voice.language, file_path = output_filename)

    return output_filename

    #reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]
    
    #pcm_audio = tts.tts(text)
    #pcm_audio = tts.tts_with_preset("your text here", voice_samples=reference_clips, preset='fast')
    
    #from tortoise.utils.audio import load_audio, load_voice