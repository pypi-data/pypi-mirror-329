from dataclasses import dataclass
from typing import Union

import json


@dataclass
class AudioTranscriptionWordTimestamp:
    """
    Class that holds the start and the end moment
    of a word said in a timestamped audio
    transcription.
    """

    start: any
    # TODO: Please set the 'start' timestamp type
    """
    The moment in which the word starts being said.
    """
    end: any
    # TODO: Please set the 'start' timestamp type
    """
    The moment in which the word ends being said.
    """

    @property
    def as_dict(
        self
    ):
        """
        Get the word timestamp as a dict.
        """
        return {
            'start': self.start,
            'end': self.end
        }

    @property
    def as_json(
        self
    ):
        """
        Get the word timestamp as a json.
        """
        return json.dumps(self.as_dict)

    def __init__(
        self,
        start: any,
        end: any
    ):
        # TODO: Please set the 'start' and 'end' timestamp type
        self.start = start
        self.end = end

@dataclass
class AudioTranscriptionWord:
    """
    Class that holds an audio transcription word
    and also its timestamp, that could be None if
    it is a non-timestamped audio transcription.
    """

    word: str
    """
    The word itself as a string.
    """
    timestamp: Union[AudioTranscriptionWordTimestamp, None]
    """
    The time moment in which the 'word' is said.
    """
    confidence: Union[float, None]
    """
    The confidence of this word being the correct
    word as a value between 0 and 1 (where 1 is 
    totally confident).
    """

    @property
    def start(
        self
    ):
        """
        The start time moment of this word.
        """
        return (
            self.timestamp.start
            if self.timestamp is not None else
            None
        )
    
    @property
    def end(
        self
    ):
        """
        The end time moment of this word.
        """
        return (
            self.timestamp.end
            if self.timestamp is not None else
            None
        )
    
    @property
    def as_dict(
        self
    ):
        """
        Get the word as a dict.
        """
        return {
            'word': self.word,
            'confidence': self.confidence,
            'start': self.start,
            'end': self.end
        }

    @property
    def as_json(
        self
    ):
        """
        Get the word as a json.
        """
        return json.dumps(self.as_dict)

    def __init__(
        self,
        word: str,
        timestamp: Union[AudioTranscriptionWordTimestamp, None] = None,
        confidence: Union[float, None] = None
    ):
        self.word = word
        self.timestamp = timestamp
        self.confidence = confidence

@dataclass
class AudioTranscription:
    """
    Class that holds information about an audio
    transcription, including words.
    """

    words: list[AudioTranscriptionWord]
    """
    The list of words.
    """

    @property
    def text(self):
        """
        Get the audio transcription as a single string
        text which is all the words concatenated.
        """
        return ' '.join([
            word.word
            for word in self.words
        ])
    
    @property
    def as_dict(
        self
    ):
        """
        Get the list of words as a dict.
        """
        return {
            'words': [
                word.as_dict
                for word in self.words
            ]
        }

    @property
    def as_json(
        self
    ):
        """
        Get the list of words as a json.
        """
        return json.dumps(self.as_dict)
