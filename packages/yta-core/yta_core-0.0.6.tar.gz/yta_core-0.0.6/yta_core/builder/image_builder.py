from yta_core.builder import Builder
from yta_core.enums.field import EnhancementField, SegmentField
from yta_core.builder.dataclasses import ClippableImage
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.downloader import Downloader
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from moviepy import VideoFileClip
from typing import Union


__all__ = [
    'ImageBuilder'
]

class ImageBuilder(Builder):
    """
    The builder of the IMAGE type.
    """

    @staticmethod
    def build_from_enhancement(
        enhancement: dict
    ):
        """
        Build the video content from the information
        in the given 'enhancement' dict.
        """
        ParameterValidator.validate_mandatory_dict('enhancement', enhancement)

        filename = enhancement.get(EnhancementField.FILENAME.value, None)
        duration = enhancement.get(EnhancementField.DURATION.value, None)
        url = enhancement.get(EnhancementField.URL.value, None)

        return (
            ImageBuilder._build_from_filename(
                filename,
                duration
            )
            if filename is not None else
            ImageBuilder._build_from_url(
                url,
                duration
            )
        )

    @staticmethod
    def build_from_segment(
        segment: dict
    ):
        """
        Build the video content from the information
        in the given 'segment' dict.
        """
        ParameterValidator.validate_mandatory_dict('segment', segment)

        filename = segment.get(SegmentField.FILENAME.value, None)
        duration = segment.get(SegmentField.DURATION.value, None)
        url = segment.get(SegmentField.URL.value, None)

        return (
            ImageBuilder._build_from_filename(
                filename,
                duration
            )
            if filename is not None else
            ImageBuilder._build_from_url(
                url,
                duration
            )
        )
    
    @classmethod
    def _build_from_filename(
        cls,
        filename: str,
        duration: Union[float, int]
    ):
        ParameterValidator.validate_mandatory_string('filename', filename, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_number('duration', duration)

        return VideoFileClip(
            ClippableImage(
                filename,
                duration,
                None
            ).video
        )

    @classmethod
    def _build_from_url(
        cls,
        url: str,
        duration: Union[float, int]
    ):
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_number('duration', duration)

        return VideoFileClip(
            ClippableImage(
                Downloader.download_image(
                    url,
                    Output.get_filename(None, FileTypeX.IMAGE)
                ).filename,
                duration,
                None
            ).video
        )