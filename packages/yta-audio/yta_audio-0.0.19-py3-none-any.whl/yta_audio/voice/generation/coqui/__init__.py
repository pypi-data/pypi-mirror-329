from yta_audio.voice.enums import NarrationLanguage
from yta_audio.voice.generation.voices import NarrationVoice
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from typing import Union
from TTS.api import TTS


class CoquiVoiceName(Enum):
    """
    Available voices. The value is what is used
    for the audio creation.
    """

    # tts_es_fastpitch_multispeaker.nemo
    # These below are the 2 Spanish models that exist
    SPANISH_MODEL_A = 'tts_models/es/mai/tacotron2-DDC'
    SPANISH_MODEL_B = 'tts_models/es/css10/vits'
    # TODO: There are more voices

class CoquiNarrationVoice(NarrationVoice):
    """
    Voice instance to be used when narrating with
    Coqui engine.
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

        CoquiVoiceName.to_enum(name)

        return name, emotion, speed, pitch, language
        
    @staticmethod
    def default():
        return CoquiNarrationVoice(CoquiVoiceName.SPANISH_MODEL_A.value, '', 130, 1.0, NarrationLanguage.DEFAULT)

VOICE_NAME_OPTIONS = [None]
LANGUAGE_OPTIONS = [
    NarrationLanguage.DEFAULT
]

# TODO: From here (https://github.com/coqui-ai/TTS)
def narrate(
    text: str,
    voice: CoquiNarrationVoice = CoquiNarrationVoice.default(),
    output_filename: Union[str, None] = None
):
    """
    Generates a narration audio file with the provided 'text' that
    will be stored as 'output_filename' file.

    This method uses a Spanish model so 'text' must be in Spanish.

    This method will take some time to generate the narration.
    """
    output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
    
    tts = TTS(model_name = voice.name)
    # There is 'language', 'emotion', 'speed'...
    tts.tts_to_file(text = text, file_path = output_filename)

    return output_filename

def narrrate_imitating_voice(
    text: str,
    input_filename: str,
    output_filename: Union[str, None] = None
):
    """
    Narrates the provided 'text' by imitating the provided 'input_filename'
    audio file (that must be a voice narrating something) and saves the 
    narration as 'output_filename'.

    The 'input_filename' could be an array of audio filenames.

    Language is set 'es' in code by default.

    This method will take time as it will recreate the voice parameters with
    which the narration will be created after that.

    ANNOTATIONS: This method is only copying the way the narration voice 
    talks, but not the own voice. This is not working as expected, as we are
    not cloning voices, we are just imitating the tone. We need another way
    to actually clone the voice as Elevenlabs do.
    """
    # TODO: This is not validating if audio file...
    if not input_filename:
        raise Exception('No "input_filename" provided.')
    
    output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    # This below will use the latest XTTS_v2 (needs to download the model)
    #tts = TTS('xtts')

    # TODO: Implement a way of identifying and storing the voices we create to
    # be able to use again them without recreating them twice.

    # input_filename can be an array of wav files
    # generate speech by cloning a voice using default settings
    tts.tts_to_file(text = text, file_path = output_filename, speaker_wav = input_filename, language = 'es')

    return output_filename