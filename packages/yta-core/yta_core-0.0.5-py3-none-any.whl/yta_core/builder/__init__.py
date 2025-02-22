from yta_core.enums.field import SegmentField
from yta_audio.voice.generation import GoogleVoiceNarrator
from yta_general_utils.programming.parameter_obtainer import ParameterObtainer
from yta_general_utils.programming.validator.parameter import ParameterValidator
from typing import Union


class Builder:
    """
    Class to wrap the general functionality about
    building elements for a project.
    """

    # TODO: Missing 'get_subclass_by_type' method

    @staticmethod
    def build_narration(
        text: str,
        output_filename: Union[str, None]
    ) -> str:
        """
        Generates a narration file that narrates the 'text' provided and
        is stored locally as 'output_filename'. If 'text' or 
        'output_filename' fields are not provided it will raise an 
        Exception.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = False)

        # TODO: This is not returning a FileReturn, I
        # think it is the filename str
        return GoogleVoiceNarrator.narrate(
            text = text,
            output_filename = output_filename
        )
    
    @staticmethod
    def get_parameters_from_method(
        method: callable,
        element: dict,
        parameters_to_ignore: list[str] = [],
        parameters_strictly_from_element: list[str] = [],
        parameters_strictly_from_extra_params: list[str] = []
    ) -> dict:
        """
        Extract the parameters from the given 'method' that are
        available in the also provided 'element' and 'extra_data',
        ignoring the ones in the 'parameters_to_ignore' list and
        applying the strategy that the other 2 'strictly' 
        parameters indicate.

        This method will return all the parameters that have been
        found only if all the mandatory ones were found, or will
        raise an Exception if some mandatory parameter is missing.

        The next parameters will be always ignored: 'self', 'cls',
        'args', 'kwargs'.

        The return value is dict in which the keys are the
        parameters names and the values, the values of those
        parameters.

        Params:
            parameters_to_ignore: The parameters we want to get
            ignored when obtained from the 'method' signature.

        Returns: 
            A dict in which the keys are the parameters names and
            the values are the values of those parameters.
        """
        ParameterValidator.validate_mandatory_dict('element', element)
        ParameterValidator.validate_mandatory_callable('method', method)
        ParameterValidator.validate_list_of_string('parameters_to_ignore', parameters_to_ignore)
        ParameterValidator.validate_list_of_string('parameters_strictly_from_element', parameters_strictly_from_element)
        ParameterValidator.validate_list_of_string('parameters_strictly_from_extra_params', parameters_strictly_from_extra_params)
        
        return get_parameters_for_method(
            method,
            element,
            parameters_to_ignore,
            parameters_strictly_from_element,
            parameters_strictly_from_extra_params
        )
    
def is_element_valid_for_method(
    method: callable,
    element: dict,
    parameters_to_ignore: list[str] = [],
    parameters_strictly_from_element: list[str] = [],
    parameters_strictly_from_extra_params: list[str] = []
) -> bool:
    # TODO: This method is too expensive as I'm doing
    # all the process again and again... It has to be
    # a more efficient way to do it
    try:
        get_parameters_for_method(
            method,
            element,
            parameters_to_ignore,
            parameters_strictly_from_element,
            parameters_strictly_from_extra_params
        )

        return True
    except:
        return False

def get_parameters_for_method(
    method: callable,
    element: dict,
    parameters_to_ignore: list[str] = [],
    parameters_strictly_from_element: list[str] = [],
    parameters_strictly_from_extra_params: list[str] = []
):
    """
    Extract the parameters from the given 'method' that are
    available in the also provided 'element' and 'extra_data',
    ignoring the ones in the 'parameters_to_ignore' list and
    applying the strategy that the other 2 'strictly' 
    parameters indicate.

    This method will return all the parameters that have been
    found only if all the mandatory ones were found, or will
    raise an Exception if some mandatory parameter is missing.

    The next parameters will be always ignored: 'self', 'cls',
    'args', 'kwargs'.

    The return value is dict in which the keys are the
    parameters names and the values, the values of those
    parameters.

    Params:
        parameters_to_ignore: The parameters we want to get
        ignored when obtained from the 'method' signature.

    Returns: 
        A dict in which the keys are the parameters names and
        the values are the values of those parameters.
    """
    # If arrays are None by any chance, turn into empty arrays
    parameters_to_ignore = [] if parameters_to_ignore is None else parameters_to_ignore
    parameters_strictly_from_element = [] if parameters_strictly_from_element is None else parameters_strictly_from_element
    parameters_strictly_from_extra_params = [] if parameters_strictly_from_extra_params is None else parameters_strictly_from_extra_params

    return _get_our_parameters_for_method(
        method = method,
        our_prepared_parameters = _get_parameters_from_element(
            element,
            parameters_strictly_from_element,
            parameters_strictly_from_extra_params
        ),
        parameters_to_ignore = parameters_to_ignore
    )

def _get_parameters_from_element(
    element: dict,
    parameters_strictly_from_element: list[str] = [],
    parameters_strictly_from_extra_params: list[str] = []
) -> dict:
    """
    Prepare the parameters from the given 'element'
    dict, applying the also given 'strictly'
    parameters to obtain the definitive ones that
    we will compare lately with the ones we need.

    This method returns the 'element' dict with the
    keys replaced as needed.
    """
    # If keys are duplicated in both 'strictly' arrays we
    # keep the one in 'from_element'
    parameters_strictly_from_extra_params = [
        parameter
        for parameter in parameters_strictly_from_extra_params
        if parameter not in parameters_strictly_from_element
    ]

    # TODO: Is this possible (?)
    extra_params = element.get(SegmentField.EXTRA_PARAMS.value, {})

    """
    We need to replace the 'element' attributes that are
    requested strictly from 'extra_params' and exist on it,
    and set in 'element' those 'extra_params' that are not
    in 'element' so we can use them.
    """

    for key, value in extra_params.items():
        if key in parameters_strictly_from_extra_params:
            element[key] = value
        elif (
            key not in parameters_strictly_from_element and
            key not in element
        ):
            element[key] = value

    return element

def _get_our_parameters_for_method(
    method: callable,
    our_prepared_parameters: dict,
    parameters_to_ignore: list[str] = []
):
    """
    Check if we have all the 'parameters_needed' in the
    given 'our_prepared_parameters' or not.

    The 'parameters_needed' are those obtained from the
    'get_parameters_needed_for_method', and the ones in
    'our_prepared_parameters' are the ones we obtain
    from 'prepare_element_parameters'.

    This method will raise an Exception if some of the
    'parameters_needed' is missing in
    'our_prepared_parameters'.
    """
    parameters_needed = ParameterObtainer.get_parameters_from_method(method, parameters_to_ignore)

    # 5. Raise exception if some mandatory param are missing
    missing_keys = set(parameters_needed.mandatory.as_dict.keys()) - set(our_prepared_parameters.keys())

    if len(missing_keys) > 0:
        print('We have found this parameters:')
        print(our_prepared_parameters)
        raise Exception(f'Some required parameters are missing: {", ".join(missing_keys)}')
    
    # TODO: Maybe rebuild as MethodParameters to return (?)
    return our_prepared_parameters
    
# TODO: We need a method just to validate if we have all 
# of them or not. Maybe it is a good choice to create
# a dataclass to hold all this complicated operations
# with parameters

