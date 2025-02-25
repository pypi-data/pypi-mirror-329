from yta_core.builder import Builder
from yta_core.enums.field import EnhancementField, SegmentField
from yta_general_utils.programming.validator.parameter import ParameterValidator
from moviepy import VideoFileClip
from typing import Union


__all__ = [
    'AIVideoBuilder'
]

class AIVideoBuilder(Builder):
    """
    The builder of the AI_VIDEO type.

    TODO: This has not been implemented yet.
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

        return AIVideoBuilder._build(
            enhancement.get(EnhancementField.KEYWORDS.value, None),
            enhancement.get(EnhancementField.DURATION.value, None)
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

        return AIVideoBuilder._build(
            segment.get(SegmentField.KEYWORDS.value, None),
            segment.get(SegmentField.DURATION.value, None)
        )
    
    @staticmethod
    def _build(
        keywords: str,
        duration: Union[float, int]
    ) -> VideoFileClip:
        """
        Build the video content with the given 'keywords'
        and 'duration'.
        """
        raise Exception('This functionality has not been implemented yet.')
        # TODO: Check how AIImageBuilder works with the
        # AIImage @dataclass and imitate it
        return VideoFileClip('test.mp4')
