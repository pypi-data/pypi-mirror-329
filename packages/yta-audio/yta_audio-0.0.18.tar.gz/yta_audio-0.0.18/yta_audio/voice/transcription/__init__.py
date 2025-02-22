"""
Audio transcription made simple by using the classes
contained in this module.
"""
from yta_audio.voice.transcription.whisper import transcribe_whisper_without_timestamps, transcribe_whisper_with_timestamps, WhisperModel
from yta_audio.voice.transcription.objects import AudioTranscriptionWord, AudioTranscription, AudioTranscriptionWordTimestamp
from yta_general_utils.programming.validator import PythonValidator
from abc import ABC, abstractmethod
from typing import Union, BinaryIO

import numpy as np


class _AudioTranscriptor(ABC):
    """
    Abstract class to be inherited by audio
    transcriptors that do not include timestamps.
    """

    @staticmethod
    @abstractmethod
    def transcribe(
        audio: any,
        initial_prompt: str
    ):
        """
        Transcribe the provided 'audio' with the help of
        the 'initial_prompt' if provided and get the
        transcripted text.
        """
        pass

class _TimestampedAudioTranscriptor(ABC):
    """
    Abstract class to be inherited by audio
    transciptors that include timestamps.
    """

    @staticmethod
    @abstractmethod
    def transcribe(
        audio: any,
        initial_prompt: str
    ):
        """
        Transcribe the provided 'audio' with the help of
        the 'initial_prompt' if provided and get the
        transcripted text with the time moments in which
        each word is detected.
        """
        pass

class DefaultAudioTranscriptor(_AudioTranscriptor):
    """
    Class to make the transcription more simple by
    choosing a transcriptor for you. You don't
    know which transcriptor you want to use? Use
    this one.
    """

    @staticmethod
    def transcribe(
        audio: Union[str, BinaryIO, np.ndarray],
        initial_prompt: Union[str, None] = None,
    ):
        return WhisperAudioTranscriptor.transcribe(audio, initial_prompt)
    
class DefaultTimestampedAudioTranscriptor(_TimestampedAudioTranscriptor):
    """
    Class to make the timestamped transcription more
    simple by choosing a timestamped transcriptor for
    you. You don't know which transcriptor you want
    to use? Use this one.
    """

    @staticmethod
    def transcribe(
        audio: Union[str, BinaryIO, np.ndarray],
        initial_prompt: Union[str, None] = None,
    ):
        return WhisperTimestampedAudioTranscriptor.transcribe(audio, initial_prompt)

class WhisperAudioTranscriptor(_AudioTranscriptor):
    """
    Whisper simple audio transcriptor that does
    not give timestamps of the the words said.
    """

    @staticmethod
    def transcribe(
        audio: Union[str, BinaryIO, np.ndarray],
        initial_prompt: Union[str, None] = None,
        model: WhisperModel = WhisperModel.BASE
    ):
        if (
            not PythonValidator.is_string(audio) and
            not PythonValidator.is_instance(audio, BinaryIO) and
            not PythonValidator.is_numpy_array(audio)
        ):
            raise Exception('The provided "audio" parameter is not a string, a BinaryIO nor a numpy array.')
        
        if (
            initial_prompt is not None and
            not PythonValidator.is_string(initial_prompt)
        ):
            raise Exception('The parameter "initial_prompt" given is not None nor a valid string.')

        transcription = transcribe_whisper_without_timestamps(audio, initial_prompt, model)

        return AudioTranscription([
            # TODO: Do I have confidence here (?)
            AudioTranscriptionWord(word, None, None)
            for word in transcription.split(' ')
        ])
    
class WhisperTimestampedAudioTranscriptor(_TimestampedAudioTranscriptor):
    """
    Whisper transcriptor that gives you the 
    timestamps of each of the transcripted words.
    """

    @staticmethod
    def transcribe(
        audio: Union[str, BinaryIO, np.ndarray],
        initial_prompt: Union[str, None] = None,
        model: WhisperModel = WhisperModel.BASE
    ):
        if (
            not PythonValidator.is_string(audio) and
            not PythonValidator.is_instance(audio, BinaryIO) and
            not PythonValidator.is_numpy_array(audio)
        ):
            raise Exception('The provided "audio" parameter is not a string, a BinaryIO nor a numpy array.')
        
        if (
            initial_prompt is not None and
            not PythonValidator.is_string(initial_prompt)
        ):
            raise Exception('The parameter "initial_prompt" given is not None nor a valid string.')

        words, _ = transcribe_whisper_with_timestamps(audio, initial_prompt, model)

        return AudioTranscription([
            AudioTranscriptionWord(word, AudioTranscriptionWordTimestamp(word['start'], word['end']), word['confidence'])
            for word in words
        ])