from yta_core.builder import Builder
from yta_core.builder.enums import Premade
from yta_core.builder.utils import enum_name_to_class
from yta_core.enums.field import EnhancementField, SegmentField
from yta_general_utils.programming.validator.parameter import ParameterValidator
from moviepy import VideoFileClip


__all__ = [
    'PremadeBuilder'
]

class PremadeBuilder(Builder):
    """
    The builder of the TEXT type.
    """

    @staticmethod
    def build_from_enhancement(
        enhancement: dict
    ) -> VideoFileClip:
        ParameterValidator.validate_mandatory_dict('enhancement', enhancement)

        return PremadeBuilder.build(
            enhancement.get(EnhancementField.KEYWORDS.value, None),
            enhancement
        )

    @staticmethod
    def build_from_segment(
        segment: dict
    ) -> VideoFileClip:
        ParameterValidator.validate_mandatory_dict('segment', segment)

        return PremadeBuilder.build(
            segment.get(SegmentField.KEYWORDS.value, None),
            segment
        )
    
    @staticmethod
    def build(
        keywords: str,
        element: dict
    ) -> VideoFileClip:
        """
        For internal use only.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        ParameterValidator.validate_mandatory_dict('element', element)

        method = enum_name_to_class(keywords, Premade).generate
        parameters = PremadeBuilder.get_parameters_from_method(method, element)

        return VideoFileClip(
            method(**parameters)
        )
        

# TODO: Remove this code below when confirmed that is not used
# def _build_custom_from_text_premade_name(
#     text_premade_name: str,
#     **parameters
# ) -> VideoFileClip:
#     """
#     This method instantiates the 'text_animation_class' Manim
#     text animation class and uses the provided 'parameters' to
#     build the text animation. The provided 'parameters' must 
#     fit the ones requested by the provided class 'generate'
#     method.
#     """
#     ParameterValidator.validate_mandatory_string('text_premade_name', text_premade_name, do_accept_empty = False)

#     # TODO: Maybe 'mask' to set background as transparent if available (?)
#     return VideoFileClip(
#         _text_premade_name_to_class(text_premade_name)().generate(**parameters)
#     )