from yta_core.builder import Builder
from yta_core.builder.dataclasses import AIImage
from yta_core.enums.field import EnhancementField, SegmentField
from yta_general_utils.programming.validator.parameter import ParameterValidator
from moviepy import concatenate_videoclips, VideoFileClip
from typing import Union


__all__ = [
    'AIImageBuilder'
]

class AIImageBuilder(Builder):
    """
    The builder of the AI_IMAGE type.
    """

    @staticmethod
    def build_from_enhancement(
        enhancement: dict
    ) -> VideoFileClip:
        """
        Build the video content from the information
        in the given 'enhancement' dict.
        """
        ParameterValidator.validate_mandatory_dict('enhancement', enhancement)

        return AIImageBuilder.build(
            enhancement.get(EnhancementField.KEYWORDS.value, None),
            enhancement.get(EnhancementField.DURATION.value, None)
        )

    @staticmethod
    def build_from_segment(
        segment: dict
    ) -> VideoFileClip:
        """
        Build the video content from the information
        in the given 'segment' dict.
        """
        ParameterValidator.validate_mandatory_dict('segment', segment)

        return AIImageBuilder.build(
            segment.get(SegmentField.KEYWORDS.value, None),
            segment.get(SegmentField.DURATION.value, None)
        )

    @staticmethod
    def build(
        keywords: str,
        duration: Union[float, int]
    ) -> VideoFileClip:
        """
        Build the video content with the given 'keywords'
        and 'duration'.
        """
        return concatenate_videoclips([
            VideoFileClip(image.video)
            for image in AIImageBuilder._get_images_array(keywords, duration)
        ])
    
    @staticmethod
    def _get_images_array(
        keywords: str,
        duration: Union[float, int],
        # TODO: Add the constant and read if from the file
        # max_duration_per_image: float = MAX_DURATION_PER_IMAGE
        max_duration_per_image: float = 5.0
    ) -> list[AIImage]:
        """
        Get a list with as many AIImage instances as needed
        to fit the provided 'duration' and according to the
        also given 'max_duration_per_image'. All those AI
        images will have been generated with the given 
        'keywords' as prompt.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)

        images: list[AIImage] = []
        if duration > max_duration_per_image:
            number_of_images = duration // max_duration_per_image
            for _ in range(number_of_images):
                images.append(AIImage(keywords, max_duration_per_image))

            remaining_duration = duration % max_duration_per_image
            if remaining_duration:
                images[-1].duration += remaining_duration  # Add to the last image's duration
            else:
                images.append(AIImage(keywords, remaining_duration))
        else:
            images.append(AIImage(keywords, duration))

        return images
