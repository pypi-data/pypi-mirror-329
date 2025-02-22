from yta_audio.silences import AudioSilence
from yta_multimedia.resources.audio.drive_urls import TYPING_KEYBOARD_3_SECONDS_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER
from yta_multimedia.resources import Resource
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from moviepy import AudioFileClip, concatenate_audioclips
from typing import Union


class SoundGenerator:

    # TODO: Move this to a consts.py file
    TYPING_SOUND_FILENAME = EFFECTS_RESOURCES_FOLDER + 'sounds/typing_keyboard_3s.mp3'

    @staticmethod
    def create_typing_audio(
        output_filename: Union[str, None] = None
    ):
        """
        Creates a typing audioclip of 3.5 seconds that, if 
        'output_filename' is provided, is stored locally
        with that name.
        """
        audio_filename = Resource.get(TYPING_KEYBOARD_3_SECONDS_GOOGLE_DRIVE_DOWNLOAD_URL, cls.TYPING_SOUND_FILENAME)
        audioclip = AudioFileClip(audio_filename)
        silence_audioclip = AudioSilence.create(0.5)

        audioclip = concatenate_audioclips([audioclip, silence_audioclip])

        if output_filename is not None:
            output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
            audioclip.write_audiofile(output_filename)

        # TODO: Maybe use FileReturn instead (?)
        return audioclip
