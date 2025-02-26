from yta_core.builder.enums import Premade, TextPremade, EffectPremade
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
    from yta_general_utils.programming.validator import PythonValidator
    print(PythonValidator.is_instance(enum, TextPremade))
    # if enum is None:
    #     raise Exception('The "enum" parameter provided is not a valid premade Enum class.')
    enum = enum.get_instance_if_name_is_accepted(premade_name, do_ignore_case = True)

    if enum is None:
        raise Exception(f'The provided premade name "{premade_name}" is not valid.')
        # raise Exception(f'The provided premade name "{premade_name}" is not valid. The valid ones are: {enum.get_all_names_as_str()}')
    
    return enum.value