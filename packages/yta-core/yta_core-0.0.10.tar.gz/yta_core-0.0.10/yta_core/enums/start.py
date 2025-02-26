from yta_general_utils.programming.enum import YTAEnum as Enum


class _Start(Enum):
    """
    The moment in which an element has to start to
    be applied.
    """

    BETWEEN_WORDS = 'between_words'
    """
    The content must be applied just in the middle 
    of two words that are dictated in the voice
    narration. This means, after the end of the 
    first word and before the start of the second
    word.
    """
    START_OF_FIRST_SHORTCODE_CONTENT_WORD = 'start_of_first_shortcode_content_word'
    """
    The content must be applied just when the first
    word of a shortcode content starts being dictated.
    """
    MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD = 'middle_of_first_shortcode_content_word'
    """
    The content must be applied just in the middle
    of the dictation of the first word of a shortcode
    content.
    """
    END_OF_FIRST_SHORTCODE_CONTENT_WORD = 'end_of_first_shortcode_content_word'
    """
    The content must be applied just when the first
    word of a shortcode content ends being dictated.
    """

class SegmentStart(Enum):
    """
    The moment in which a Segment has to start to
    be applied.
    """

    pass

# TODO: Review this (maybe rename as it is for shortcodes, 
# not enhancement elements yet).
class EnhancementStart(Enum):
    """
    The moment in which an Enhancement has to start to
    be applied.
    """

    pass
    
class ShortcodeStart(Enum):
    """
    The moment in which a Shortcode has to start to
    be applied.
    """

    BETWEEN_WORDS = _Start.BETWEEN_WORDS.value
    """
    The content must be applied just in the middle 
    of two words that are dictated in the voice
    narration. This means, after the end of the 
    first word and before the start of the second
    word.
    """
    START_OF_FIRST_SHORTCODE_CONTENT_WORD = _Start.START_OF_FIRST_SHORTCODE_CONTENT_WORD.value
    """
    The content must be applied just when the first
    word of a shortcode content starts being dictated.
    """
    MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD = _Start.MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD.value
    """
    The content must be applied just in the middle
    of the dictation of the first word of a shortcode
    content.
    """
    END_OF_FIRST_SHORTCODE_CONTENT_WORD = _Start.END_OF_FIRST_SHORTCODE_CONTENT_WORD.value
    """
    The content must be applied just when the first
    word of a shortcode content ends being dictated.
    """

    @classmethod
    def get_default(cls):
        return cls.START_OF_FIRST_SHORTCODE_CONTENT_WORD