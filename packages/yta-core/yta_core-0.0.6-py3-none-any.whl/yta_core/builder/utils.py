from yta_core.builder.enums import Premade, TextPremade, EffectPremade
from yta_general_utils.programming.validator.parameter import ParameterValidator
from typing import Union


def enum_name_to_class(
    premade_name: str,
    enum: Union[Premade, TextPremade, EffectPremade]
):
    """
    Turn the provided 'premade_name' to its corresponding
    premade Enum and obtain the class that can be used to
    build the video.

    This method will return None if the 'premade_name' is
    not valid, or the class if it is.
    """
    ParameterValidator.validate_mandatory_class_of(
        'enum',
        enum,
        [Premade, TextPremade, EffectPremade]
    )

    valid_name = enum.get_valid_name(premade_name)

    if not valid_name:
        raise Exception(f'The provided premade name "{premade_name}" is not valid. The valid ones are: {enum.get_all_names_as_str()}')
    
    return enum[valid_name].value