"""
Utils for audio conversion.
"""
from yta_general_utils.temp import Temp
from yta_general_utils.programming.validator import PythonValidator
from moviepy import AudioFileClip, AudioClip
from pydub import AudioSegment

import io
import scipy.io.wavfile as wavfile
import numpy as np


def audiosegment_to_audioclip(audio: AudioSegment):
    """
    Export the 'audio' AudiOSegment to a file and
    read it as a moviepy audio file.

    TODO: Please, make it through memory and not writting files.
    """
    if not PythonValidator.is_instance(audio, AudioSegment):
        raise Exception('The "audio" parameter provided is not an AudioSegment.')
    
    # TODO: I have not been able to create an AudioFileClip dinamically
    # from memory information. I don't want to write but...
    tmp_filename = Temp.create_filename('tmp_audio.wav')
    audio.export(tmp_filename, format = 'wav')

    return AudioFileClip(tmp_filename)

def audioclip_to_audiosegment(audio: AudioClip):
    """
    This method returns the provided moviepy audio converted into a
    pydub AudioSegment.

    TODO: This method currently writes a temporary file to make the 
    conversion. This needs to be improved to avoid writting files.
    """
    if not PythonValidator.is_instance(audio, AudioClip):
        raise Exception('The provided "audio" parameter is not an AudioClip.')

    # TODO: Please, improve this to be not writting files
    tmp_filename = Temp.create_filename('tmp_audio.wav')
    audio.write_audiofile(tmp_filename)
    audio = AudioSegment.from_file(tmp_filename, format = 'wav')

    return audio

# TODO: This has not been tested properly
def numpy_to_audiosegment(audio: np.ndarray, sample_rate):
    """
    Convers the provided 'audio' numpy array,
    that contains the audio data and must be in
    float32 or int16, to a pydub AudioSegment.

    TODO: Untested method
    """
    if not PythonValidator.is_instance(audio, np.ndarray):
        raise Exception('The "audio" parameter provided is not an np.ndarray.')
    
    # Normalize audio_array if it's not already in int16 format
    if audio.dtype != np.int16:
        if audio.dtype != np.float32:
            raise Exception('The "audio" parameter provided is not np.int16 nor np.float32.')
        
        # Assuming the audio_array is in float32 with values between -1 and 1
        audio = (audio * 32767).astype(np.int16)
    
    with io.BytesIO() as buffer:
        wavfile.write(buffer, sample_rate, audio)
        buffer.seek(0)
        
        audio_segment = AudioSegment.from_file(buffer, format = 'wav')
    
    return audio_segment

def audiosegment_to_numpy(audio: AudioSegment):
    """
    This method turns the provided 'audio' AudioSegment into a numpy
    array by converting it first to an AudioFileClip and then to a
    numpy.

    TODO: Please, maybe it is a better (more direct) way

    TODO: This method has not been tested properly
    """
    if not PythonValidator.is_instance(audio, AudioSegment):
        raise Exception('The provided "audio" parameter is not an AudioSegment.')
    
    # TODO: Maybe this is not the best way, I need
    # to test and improve this
    return np.array(audio.get_array_of_samples())

def numpy_to_audioclip(audio: np.ndarray):
    """
    This method turns the provided 'audio' np.ndarray
    into a moviepy AudioClip.

    TODO: This method has not been tested properly
    """
    if not PythonValidator.is_instance(audio, np.ndarray):
        raise Exception('The provided "audio" parameter is not an np.ndarray.')
    
    # TODO: This is untested, make it work
    return AudioClip(audio)

def audioclip_to_numpy(audio: AudioClip):
    """
    Convers the provided 'audio' moviepy AudioFileClip to a numpy
    array that will be np.float32.
    """
    if not PythonValidator.is_instance(audio, AudioClip):
        raise Exception('The provided "audio" parameter is not an AudioClip.')
    
    # TODO: Check this: https://github.com/Zulko/moviepy/issues/2027#issuecomment-1937357458

    chunk_size = 5 * 1024 * 1024
    audio_chunks = []
    for chunk in audio.iter_chunks(chunksize = chunk_size):
        # Convertir cada fragmento a un array numpy y añadirlo a la lista
        audio_array = np.frombuffer(chunk, dtype=np.int16)
        
        # Normalizar si el audio es estéreo (tendría dos columnas)
        if len(audio_array) > 0 and len(audio_array) % 2 == 0:
            audio_array = audio_array.reshape(-1, 2)
        
        audio_chunks.append(audio_array)
    
    # Concatenar todos los fragmentos en un solo array
    full_audio_array = np.concatenate(audio_chunks, axis = 0)
    
    # Convertir a float32 y normalizar
    full_audio_array = full_audio_array.astype(np.float32)
    if np.max(np.abs(full_audio_array)) > 1.0:
        full_audio_array /= np.max(np.abs(full_audio_array))
    
    return full_audio_array


def is_audio_valid(audio: list[str, np.ndarray, AudioSegment, AudioFileClip]):
    if not PythonValidator.is_string(audio) and not PythonValidator.is_instance(audio, [np.ndarray, AudioSegment, AudioFileClip]):
        return False
    
    return True

def validate_audio(audio: list[str, np.ndarray, AudioSegment, AudioFileClip]):
    # TODO: Not only 'AudioFileClip', better 'AudioClip'
    if not is_audio_valid(audio):
        raise Exception('The provided "audio" is not valid. It must be one of these clases: "str, np.ndarray, AudioSegment, AudioFileClip".')
    


__all__ = [
    'audiosegment_to_audioclip',
    'audioclip_to_audiosegment',
    'numpy_to_audiosegment',
    'audiosegment_to_numpy',
    'numpy_to_audioclip',
    'audioclip_to_numpy',
    'is_audio_valid',
    'validate_audio'
]