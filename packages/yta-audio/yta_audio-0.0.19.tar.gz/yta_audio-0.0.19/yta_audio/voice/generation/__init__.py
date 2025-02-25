from yta_audio.voice.generation.voices import NarrationVoice
from yta_audio.voice.generation.coqui import narrate as narrate_coqui, CoquiNarrationVoice
from yta_audio.voice.generation.google import narrate as narrate_google, GoogleNarrationVoice
from yta_audio.voice.generation.microsoft import narrate as narrate_microsoft, MicrosoftNarrationVoice
from yta_audio.voice.generation.open_voice import narrate as narrate_open_voice, OpenVoiceNarrationVoice
from yta_audio.voice.generation.tetyys import narrate_tetyys, TetyysNarrationVoice
from yta_audio.voice.generation.tiktok import narrate_tiktok, TiktokNarrationVoice
from yta_audio.voice.generation.tortoise import narrate as narrate_tortoise, TortoiseNarrationVoice
from yta_audio.voice.generation.ttsmp3 import narrate_tts3, Ttsmp3NarrationVoice
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.temp import Temp
from abc import ABC, abstractmethod
from typing import Union


class VoiceNarrator(ABC):
    """
    Class to simplify and encapsulate the voice
    narration functionality.
    """

    @staticmethod
    @abstractmethod
    def narrate(
        text: str,
        voice: NarrationVoice = NarrationVoice.default(),
        output_filename: Union[str, None] = None
    ):
        """
        Create a voice narration of the given 'text' and
        stores it locally in the 'output_filename'
        provided (or in a temporary file if not provided).
        """
        pass

class CoquiVoiceNarrator(VoiceNarrator):

    @staticmethod
    def narrate(
        text: str,
        voice: CoquiNarrationVoice = CoquiNarrationVoice.default(),
        output_filename: Union[str, None] = None
    ):
        if not PythonValidator.is_string(text):
            raise Exception('No valid "text" parameter provided.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        
        # TODO: Maybe return a FileReturn (?)
        return narrate_coqui(text, voice, output_filename = output_filename)
    
class GoogleVoiceNarrator(VoiceNarrator):

    @staticmethod
    def narrate(
        text: str,
        voice: GoogleNarrationVoice = GoogleNarrationVoice.default(),
        output_filename: Union[str, None] = None
    ):
        # TODO: Include 'language' and 'tld' as parameters
        if not PythonValidator.is_string(text):
            raise Exception('No valid "text" parameter provided.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        
        # TODO: Maybe return a FileReturn (?)
        return narrate_google(text, voice, output_filename = output_filename)
    
class MicrosoftVoiceNarrator(VoiceNarrator):

    @staticmethod
    def narrate(
        text: str,
        voice: MicrosoftNarrationVoice = MicrosoftNarrationVoice.default(),
        output_filename: Union[str, None] = None
    ):
        # TODO: Include 'language' and 'tld' as parameters
        if not PythonValidator.is_string(text):
            raise Exception('No valid "text" parameter provided.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        
        # TODO: Maybe return a FileReturn (?)
        return narrate_microsoft(text, voice, output_filename = output_filename)
    
class OpenVoiceVoiceNarrator(VoiceNarrator):

    @staticmethod
    def narrate(
        text: str,
        voice: OpenVoiceNarrationVoice = OpenVoiceNarrationVoice.default(),
        output_filename: Union[str, None] = None
    ):
        # TODO: Include 'speed' as parameter
        if not PythonValidator.is_string(text):
            raise Exception('No valid "text" parameter provided.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        
        # TODO: Maybe return a FileReturn (?)
        return narrate_open_voice(text, voice, output_filename = output_filename)
    
class TetyysVoiceNarrator(VoiceNarrator):

    @staticmethod
    def narrate(
        text: str,
        voice: TetyysNarrationVoice = TetyysNarrationVoice.default(),
        output_filename: Union[str, None] = None
    ):
        # TODO: Include 'speed' as parameter
        if not PythonValidator.is_string(text):
            raise Exception('No valid "text" parameter provided.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        
        # TODO: Maybe return a FileReturn (?)
        return narrate_tetyys(text, voice, output_filename = output_filename)
    
class TiktokVoiceNarrator(VoiceNarrator):

    @staticmethod
    def narrate(
        text: str,
        voice: TiktokNarrationVoice = TiktokNarrationVoice.default(),
        output_filename: Union[str, None] = None
    ):
        # TODO: Include 'speed' as parameter
        if not PythonValidator.is_string(text):
            raise Exception('No valid "text" parameter provided.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        
        # TODO: Maybe return a FileReturn (?)
        return narrate_tiktok(text, voice, output_filename = output_filename)
    
class TortoiseVoiceNarrator(VoiceNarrator):

    @staticmethod
    def narrate(
        text: str,
        voice: TortoiseNarrationVoice = TortoiseNarrationVoice.default(),
        output_filename: Union[str, None] = None
    ):
        # TODO: Include 'speed' as parameter
        if not PythonValidator.is_string(text):
            raise Exception('No valid "text" parameter provided.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        
        # TODO: Maybe return a FileReturn (?)
        return narrate_tortoise(text, voice, output_filename = output_filename)
    
class Ttsmp3VoiceNarrator(VoiceNarrator):

    @staticmethod
    def narrate(
        text: str,
        voice: Ttsmp3NarrationVoice = Ttsmp3NarrationVoice.default(),
        output_filename: Union[str, None] = None
    ):
        # TODO: Include 'speed' as parameter
        if not PythonValidator.is_string(text):
            raise Exception('No valid "text" parameter provided.')
        
        output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        
        # TODO: Maybe return a FileReturn (?)
        return narrate_tts3(text, voice, output_filename = output_filename)