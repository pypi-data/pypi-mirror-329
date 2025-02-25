"""
# Very interesting (https://github.com/m-bain/whisperX) to get timestamps of each word
# But the one I use is this one (https://github.com/linto-ai/whisper-timestamped)
"""
from yta_general_utils.programming.enum import YTAEnum as Enum
from faster_whisper import WhisperModel
from typing import Union, BinaryIO

import whisper_timestamped
import numpy as np


class WhisperModel(Enum):
    """
    The model of Whisper you want to use to detect
    the audio.

    See more:
    https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages
    """
    
    TINY = 'tiny'
    """
    Trained with 39M parameters.
    Required VRAM: ~1GB.
    Relative speed: ~10x.
    """
    BASE = 'base'
    """
    Trained with 74M parameters.
    Required VRAM: ~1GB.
    Relative speed: ~7x.
    """
    SMALL = 'small'
    """
    Trained with 244M parameters.
    Required VRAM: ~2GB.
    Relative speed: ~4x.
    """
    MEDIUM = 'medium'
    """
    Trained with 769M parameters.
    Required VRAM: ~5GB.
    Relative speed: ~2x.
    """
    LARGE = 'large'
    """
    Trained with 1550M parameters.
    Required VRAM: ~10GB.
    Relative speed: ~1x.
    """
    TURBO = 'turbo'
    """
    Trained with 809M parameters.
    Required VRAM: ~6GB.
    Relative speed: ~8x.
    """

def transcribe_whisper_with_timestamps(
    audio: Union[str, BinaryIO, np.ndarray],
    initial_prompt: Union[str, None] = None,
    model: WhisperModel = WhisperModel.BASE
):
    """
    Transcribe the provided 'audio' using the specified
    'model' and obtains a list of 'words' (with the
    'start' and 'end' times) and the whole 'text' in
    the audio.

    This method returns the tuple (words, text).
    """
    model = WhisperModel.to_enum(model)

    audio = whisper_timestamped.load_audio(audio)
    model = whisper_timestamped.load_model(model.value, device = 'cpu')

    # See this: https://github.com/openai/openai-cookbook/blob/main/examples/Whisper_prompting_guide.ipynb
    # I do this 'initial_prompt' formatting due to some issues when using it 
    # as it was. I read in Cookguide to pass natural sentences like this below
    # and it seems to be working well, so here it is:
    if initial_prompt is not None:
        #initial_prompt = '""""' + initial_prompt + '""""'
        #initial_prompt = 'I know exactly what is said in this audio and I will give it to you (between double quotes) to give me the exact transcription. The audio says, exactly """"' + initial_prompt + '""""'
        initial_prompt = 'I will give you exactly what the audio says (the output), so please ensure it fits. The output must be """"' + initial_prompt + '""""'

    # 'vad' = True would remove silent parts to decrease hallucinations
    # 'detect_disfluences' detects corrections, repetitions, etc. so the
    # word prediction should be more accurate. Useful for natural narrations
    transcription = whisper_timestamped.transcribe(model, audio, language = "es", initial_prompt = initial_prompt)
    """
    'text', which includes the whole text
    'segments', which has the different segments
    'words', inside 'segments', which contains each 
    word and its 'text', 'start' and 'end'
    """
    words = [word for segment in transcription['segments'] for word in segment['words']]
    text = ' '.join([word['text'] for word in words])

    return words, text
    
def transcribe_whisper_without_timestamps(
    audio: Union[str, BinaryIO, np.ndarray],
    initial_prompt: Union[str, None] = None,
    model: WhisperModel = WhisperModel.BASE
):
    """
    Obtain the transcription with no timestamps, fast and
    ideal to get ideas from the text, summarize it, etc.

    I recommend you using the 'transcribe_with_timestamps'
    because the result is more complete.

    The result is just the transcription as a text.
    """
    # TODO: What if 'whisper_timestamped' is better? We should use it
    # TODO: Create FasterWhisperModel Enum and add to params
    model = WhisperModel('base')

    if initial_prompt is not None:
        #initial_prompt = '""""' + initial_prompt + '""""'
        #initial_prompt = 'I know exactly what is said in this audio and I will give it to you (between double quotes) to give me the exact transcription. The audio says, exactly """"' + initial_prompt + '""""'
        initial_prompt = 'I will give you exactly what the audio says (the output), so please ensure it fits. The output must be """"' + initial_prompt + '""""'

    segments, _ = model.transcribe(audio, language = 'es', beam_size = 5, initial_prompt = initial_prompt)

    text = ' '.join([
        segment.text
        for segment in segments
    ]).strip()

    return text