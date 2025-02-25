from yta_core.builder import Builder
from yta_core.builder.enums import EffectPremade
from yta_core.enums.field import EnhancementField
from yta_core.builder.utils import enum_name_to_class
from yta_general_utils.programming.validator.parameter import ParameterValidator


__all__ = [
    'EffectBuilder'
]

class EffectBuilder(Builder):
    """
    The builder of the EFFECT type.
    """

    @staticmethod
    def build_from_enhancement(
        enhancement: dict
    ):
        ParameterValidator.validate_mandatory_dict('enhancement', enhancement)

        keywords = enhancement.get(EnhancementField.KEYWORDS.value, None)

        return EffectBuilder.build(keywords)
    
    @staticmethod
    def build(
        keywords: str
    ):
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)

        # TODO: This is not working, it does nothing but
        # obtaining the effect
        return enum_name_to_class(keywords, EffectPremade)