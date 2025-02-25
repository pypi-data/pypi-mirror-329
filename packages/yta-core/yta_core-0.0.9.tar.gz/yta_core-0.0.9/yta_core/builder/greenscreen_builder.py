from yta_core.builder import Builder
from yta_core.enums.field import EnhancementField
from yta_multimedia.greenscreen.custom.greenscreen import Greenscreen
from yta_general_utils.programming.validator.parameter import ParameterValidator


__all__ = [
    'GreenscreenBuilder'
]

class GreenscreenBuilder(Builder):
    """
    The builder of the GREENSCREEN type.
    """

    @staticmethod
    def build_from_enhancement(
        enhancement: dict
    ):
        """
        Get an ImageGreenscreen or VideoGreenscreen instance
        initialized with the provided 'filename' or 'url'
        (filename has priority) or raises an Exception if
        something goes wrong.
        """
        ParameterValidator.validate_mandatory_dict('enhancement', enhancement)

        filename = enhancement.get(EnhancementField.FILENAME.value, None)
        url = enhancement.get(EnhancementField.URL.value, None)

        if url is None and filename is None:
            # TODO: I think this cannot happen
            raise Exception('No "url" nor "filename" provided and at least one is needed.')

        return (
            Greenscreen.init(url)
            if url and not filename else
            Greenscreen.init(filename)
        )