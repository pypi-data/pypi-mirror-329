from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.text.finder import TextFinderMode as EditionManualTermMode


__all__ = [
    'EditionManualTermContext',
    'EditionManualTermField',
    'EditionManualTermMode'
]

class EditionManualTermContext(Enum):
    """
    This is the context our edition terms will have.
    The context will determine in which text topics
    we will need to apply the edition term.
    """
    
    ANY = 'any'
    """
    The term will be applied always, in any context.
    """
    
    @classmethod
    def get_default(
        cls
    ):
        """
        Get the item by default.
        """
        return cls.ANY

class EditionManualTermField(Enum):
    """
    Enum class to wrap the different fields an
    edition manual term can have.
    """

    MODE = 'mode'
    """
    The mode in which the edition manual term
    has to be searched to match the context of
    the text. Check the 'TextFinderMode' Enum
    class in TextFinder.
    """
    CONTEXT = 'context'
    """
    The context in which the the edition manual
    term should be applied, that could be a
    a topic, a category, etc.
    """
    ENHANCEMENTS = 'enhancements'
    """
    The content enhancements that must be 
    applied when this eidion manual term has
    to.
    """