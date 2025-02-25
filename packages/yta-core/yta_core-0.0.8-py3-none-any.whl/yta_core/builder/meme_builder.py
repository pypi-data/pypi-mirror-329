from yta_core.builder import Builder
from yta_core.builder.youtube import YoutubeDownloader
from yta_core.enums.field import EnhancementField, SegmentField
from yta_general_utils.programming.validator.parameter import ParameterValidator
from moviepy import VideoFileClip
from typing import Union


__all__ = [
    'MemeBuilder'
]

class MemeBuilder(Builder):
    """
    The builder of the MEME type.
    """

    @staticmethod
    def build_from_enhancement(
        enhancement: dict
    ) -> VideoFileClip:
        ParameterValidator.validate_mandatory_dict('enhancement', enhancement)

        return MemeBuilder.build(
            enhancement.get(EnhancementField.KEYWORDS.value, None),
            enhancement.get(EnhancementField.DURATION.value, None)
        )

    @staticmethod
    def build_from_segment(
        segment: dict
    ) -> VideoFileClip:
        ParameterValidator.validate_mandatory_dict('segment', segment)

        return MemeBuilder.build(
            segment.get(SegmentField.KEYWORDS.value, None),
            segment.get(SegmentField.DURATION.value, None)
        )

    @classmethod
    def build(
        cls,
        keywords: str,
        duration: Union[float, int]
    ) -> VideoFileClip:
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_number('duration', duration)

        youtube_downloader = YoutubeDownloader()

        youtube_downloader.deactivate_ignore_repeated()
        temp_filename = youtube_downloader.download_meme_video(keywords, True, True)
        youtube_downloader.activate_ignore_repeated()

        # TODO: Look for a better strategy (?)
        if not temp_filename:
            raise Exception(f'No meme found with the given "keywords": {keywords}.')
        
        video = VideoFileClip(temp_filename)

        return (
            video.with_subclip(0, duration)
            if duration < video.duration else
            video
        )