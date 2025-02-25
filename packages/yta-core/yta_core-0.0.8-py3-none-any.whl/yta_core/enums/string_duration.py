from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.validator.parameter import ParameterValidator


class _StringDuration(Enum):
    """
    Enum class to represent the different strings
    that we accept as duration values for the
    pre-processing moment. These strings will be
    transformed in a numeric value when we are able
    to do it (maybe we need to download a file, to
    create a voice narration, etc.).

    For internal use only. Use a more specific
    Enum class to interact with the different
    string durations.
    """

    SEGMENT_DURATION = 99999
    """
    The duration is expected to be the whole segment
    duration, that is only known once we have built
    it. This is, for example, useful for a music that
    we want to apply during a whole segment, or maybe
    a watermark we want to place also during the
    segment duration.
    """
    FILE_DURATION = 99998
    """
    The duration is expected to be the source file 
    (downloaded or obtained from the local system)
    duration.
    """
    SHORTCODE_CONTENT = 99997
    """
    The duration is expected to be from the begining
    of the shortcode content (start of first word) to
    the end of it (end of last word).
    """

    @staticmethod
    def to_numeric_value(
        duration: str
    ) -> int:
        """
        Transform the provided string 'duration' parameter
        to its actual numeric value according to our Enum
        declaration, or raises an Exception if not valid.
        This numeric value will be later processed by our
        system and transformed to the real duration when
        calculated.
        """
        ParameterValidator.validate_mandatory_string('duration', duration)

        duration = {
            _StringDuration.SHORTCODE_CONTENT.name.lower(): _StringDuration.SHORTCODE_CONTENT.value,
            _StringDuration.FILE_DURATION.name.lower(): _StringDuration.FILE_DURATION.value,
            _StringDuration.SEGMENT_DURATION.name.lower(): _StringDuration.SEGMENT_DURATION.value
        }.get(duration.lower(), None)

        if duration is None:
            raise Exception(f'The provided "duration" parameter {duration} is not a valid StringDuration name.')
        
        return duration
    
class SegmentStringDuration(Enum):
    """
    The string durations accepted within a Segment.
    """

    FILE_DURATION = _StringDuration.FILE_DURATION.value
    """
    The duration is expected to be the source file 
    (downloaded or obtained from the local system)
    duration.
    """

    @staticmethod
    def to_numeric_value(
        duration: str
    ):
        """
        Transform the provided string 'duration' parameter
        to its actual numeric value according to our Enum
        declaration, or raises an Exception if not valid.
        This numeric value will be later processed by our
        system and transformed to the real duration when
        calculated.
        """
        _StringDuration.to_numeric_value(duration)

class EnhancementStringDuration(Enum):
    """
    The string durations accepted within an 
    Enhancement.
    """

    FILE_DURATION = _StringDuration.FILE_DURATION.value
    """
    The duration is expected to be the source file 
    (downloaded or obtained from the local system)
    duration.
    """
    SEGMENT_DURATION = _StringDuration.SEGMENT_DURATION.value
    """
    The duration is expected to be the whole segment
    duration, that is only known once we have built
    it. This is, for example, useful for a music that
    we want to apply during a whole segment, or maybe
    a watermark we want to place also during the
    segment duration.
    """

    @staticmethod
    def to_numeric_value(
        duration: str
    ):
        """
        Transform the provided string 'duration' parameter
        to its actual numeric value according to our Enum
        declaration, or raises an Exception if not valid.
        This numeric value will be later processed by our
        system and transformed to the real duration when
        calculated.
        """
        _StringDuration.to_numeric_value(duration)

class ShortcodeStringDuration(Enum):
    """
    The string durations accepted within a Shortcode.
    """
    
    FILE_DURATION = _StringDuration.FILE_DURATION.value
    """
    The duration is expected to be the source file 
    (downloaded or obtained from the local system)
    duration.
    """
    SEGMENT_DURATION = _StringDuration.SEGMENT_DURATION.value
    """
    The duration is expected to be the whole segment
    duration, that is only known once we have built
    it. This is, for example, useful for a music that
    we want to apply during a whole segment, or maybe
    a watermark we want to place also during the
    segment duration.
    """
    SHORTCODE_CONTENT = _StringDuration.SHORTCODE_CONTENT.value
    """
    The duration is expected to be from the begining
    of the shortcode content (start of first word) to
    the end of it (end of last word).
    """

    @staticmethod
    def to_numeric_value(
        duration: str
    ):
        """
        Transform the provided string 'duration' parameter
        to its actual numeric value according to our Enum
        declaration, or raises an Exception if not valid.
        This numeric value will be later processed by our
        system and transformed to the real duration when
        calculated.
        """
        _StringDuration.to_numeric_value(duration)