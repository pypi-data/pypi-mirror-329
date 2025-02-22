from yta_core.builder import Builder
from yta_core.builder.youtube import YoutubeDownloader
from yta_core.enums.field import EnhancementField, SegmentField
from yta_general_utils.programming.validator.parameter import ParameterValidator
from moviepy import AudioFileClip
from typing import Union


__all__ = [
    'SoundBuilder'
]

class SoundBuilder(Builder):
    """
    The builder of the SOUND type.
    """

    @staticmethod
    def build_from_enhancement(
        enhancement: dict
    ) -> AudioFileClip:
        ParameterValidator.validate_mandatory_dict('enhancement', enhancement)

        return SoundBuilder.build(
            enhancement.get(EnhancementField.KEYWORDS.value, None),
            enhancement.get(EnhancementField.DURATION.value, None)
        )

    @staticmethod
    def build_from_segment(
        segment: dict
    ) -> AudioFileClip:
        ParameterValidator.validate_mandatory_dict('segment', segment)

        return SoundBuilder.build(
            segment.get(SegmentField.KEYWORDS.value, None),
            segment.get(SegmentField.DURATION.value, None)
        )

    @staticmethod
    def build(
        keywords: str,
        duration: Union[float, int]
    ) -> AudioFileClip:
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_number('duration', duration)

        youtube_downloader = YoutubeDownloader()

        youtube_downloader.deactivate_ignore_repeated()
        temp_filename = youtube_downloader.download_sound_audio(keywords)
        youtube_downloader.activate_ignore_repeated()

        # TODO: Look for a better strategy (?)
        if not temp_filename:
            raise Exception(f'No sound found with the given "keywords": {keywords}.')
        
        audio = AudioFileClip(temp_filename)

        return (
            audio.with_subclip(0, duration)
            if duration < audio.duration else
            audio
        )