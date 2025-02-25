"""
Module to include all the validation classes
that simplify the way we check if the provided
jsons are valid and accepted by our system or
not to build the Segment, Enhancement and/or
Shortcode components.
"""
from yta_core.configuration import Configuration
from yta_core.builder.utils import enum_name_to_class
from yta_core.builder import is_element_valid_for_method
from yta_core.builder.enums import Premade, TextPremade
from yta_core.shortcodes.parser import shortcode_parser, empty_shortcode_parser
from yta_core.enums.field import SegmentField, EnhancementField, ShortcodeField
from yta_core.enums.mode import SegmentMode, EnhancementMode, ShortcodeMode
from yta_core.enums.type import SegmentType, EnhancementType, ShortcodeType
from yta_core.enums.string_duration import SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration
from yta_core.enums.component import Component
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.programming.validator import PythonValidator
from typing import Union


class BuilderValidator:
    """
    Class to validate everything related to segments,
    enhancements and shortcodes. A single source of
    validation.
    """

    @staticmethod
    def validate_segment_has_expected_fields(
        segment: dict
    ) -> None:
        """
        Check if the provided 'segment' dict has all the
        fields it must have as a Segment, and raises an
        Exception if not.
        """
        return BuilderValidator._validate_component_has_expected_fields(
            segment,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_enhancement_has_expected_fields(
        enhancement: dict
    ) -> None:
        """
        Check if the provided 'enhancement' dict has all the
        fields it must have as an Enhancement, and raises an
        Exception if not.
        """
        return BuilderValidator._validate_component_has_expected_fields(
            enhancement,
            Component.ENHANCEMENT
        )
    
    @staticmethod
    def validate_shortcode_has_expected_fields(
        shortcode: dict
    ) -> None:
        """
        Check if the provided 'shortcode' dict has all the
        fields it must have as a Shortcode, and raises an
        Exception if not.
        """
        return BuilderValidator._validate_component_has_expected_fields(
            shortcode,
            Component.SHORTCODE
        )

    @staticmethod
    def _validate_component_has_expected_fields(
        element: dict,
        component: Component
    ) -> None:
        """
        Check if the provided 'element' dict, that must be
        a dict representing the 'component' passed as 
        parameter, has all the fields it must have, and 
        raises an Exception if not.

        This method will detect the parameters that exist
        in the provided 'element' but are not expected to
        be on it, and the ones that are expected to be but
        are not set on it.
        """
        component = Component.to_enum(component)
        ParameterValidator.validate_mandatory_dict('element', element)

        accepted_fields = {
            Component.SEGMENT: lambda: SegmentField.get_all_values(),
            Component.ENHANCEMENT: lambda: EnhancementField.get_all_values(),
            Component.SHORTCODE: lambda: ShortcodeField.get_all_values()
        }[component]()

        accepted_fields_str = ', '.join(accepted_fields)

        unaccepted_fields = [
            key
            for key in element.keys()
            if key not in accepted_fields
        ]
        unaccepted_fields_str = ', '.join(unaccepted_fields)
        
        missing_fields = [
            field
            for field in accepted_fields
            if field not in element
        ]
        missing_fields_str = ', '.join(missing_fields)

        if missing_fields:
            raise Exception(f'The next fields are mandatory and were not found in the element: "{missing_fields_str}". The mandatory fields are: "{accepted_fields_str}".')

        if unaccepted_fields:
            raise Exception(f'The next fields are not accepted in the provided element by our system: "{unaccepted_fields_str}". The ones accepted are these: "{accepted_fields_str}".')
        
        return element
    
    # MODE below
    @staticmethod
    def validate_segment_mode_field(
        mode: Union[SegmentMode, str, None]
    ):
        """
        Validate the provided 'mode' for a Segment
        component.

        This method will raise an exception if the 
        'mode' provided is not valid.
        """
        return BuilderValidator._validate_component_mode_field(
            mode,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_enhancement_mode_field(
        mode: Union[EnhancementMode, str, None]
    ):
        """
        Validate the provided 'mode' for an Enhancement
        component.

        This method will raise an exception if the 
        'mode' provided is not valid.
        """
        return BuilderValidator._validate_component_mode_field(
            mode,
            Component.ENHANCEMENT
        )
    
    @staticmethod
    def validate_shortcode_mode_field(
        mode: Union[ShortcodeMode, str, None]
    ):
        """
        Validate the provided 'mode' for a Shortcode
        component.

        This method will raise an exception if the 
        'mode' provided is not valid.
        """
        return BuilderValidator._validate_component_mode_field(
            mode,
            Component.SHORTCODE
        )

    @staticmethod
    def _validate_component_mode_field(
        mode: Union[SegmentMode, EnhancementMode, ShortcodeMode, str, None],
        component: Component
    ):
        """
        Validate the provided 'mode' for the given
        'component'. The mode should be a SegmentMode,
        EnhancementMode or ShortcodeMode, or a string
        that fits one of these 3 enum classes.

        This method will raise an exception if the 
        'mode' provided is not valid for the given
        'component'.
        """
        component = Component.to_enum(component)

        # TODO: Do we accept 'None' value (?)
        return component.get_mode(mode)
    
    # MODE FOR TYPE below
    @staticmethod
    def validate_segment_mode_for_type(
        mode: Union[SegmentMode, str, None],
        type: Union[SegmentType, str]
    ):
        """
        Validate if the provided 'mode' is accepted by
        the also given 'type' for a Segment.
        """
        return BuilderValidator._validate_component_mode_for_type(
            mode,
            type,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_enhancement_mode_for_type(
        mode: Union[EnhancementMode, str, None],
        type: Union[EnhancementType, str]
    ):
        """
        Validate if the provided 'mode' is accepted by
        the also given 'type' for an Enhancement.
        """
        return BuilderValidator._validate_component_mode_for_type(
            mode,
            type,
            Component.ENHANCEMENT
        )
    
    @staticmethod
    def validate_shortcode_mode_for_type(
        mode: Union[ShortcodeMode, str, None],
        type: Union[ShortcodeType, str]
    ):
        """
        Validate if the provided 'mode' is accepted by
        the also given 'type' for an Shortcode.
        """
        return BuilderValidator._validate_component_mode_for_type(
            mode,
            type,
            Component.SHORTCODE
        )
    
    @staticmethod
    def _validate_component_mode_for_type(
        mode: Union[SegmentMode, EnhancementMode, ShortcodeMode, str, None],
        type: Union[SegmentType, EnhancementType, ShortcodeType, str],
        component: Component
    ):
        """
        Validate if the provided 'mode' is accepted by
        the also given 'type' for the also provided
        'component'.
        """
        component = Component.to_enum(component)

        if not component.is_mode_accepted_for_type(mode, type):
            type = (
                type
                if PythonValidator.is_string(type) else
                type.value
            )

            raise Exception(f'The "{type}" type does not accept the provided "{mode}" mode.')

    # DURATION below
    @staticmethod
    def validate_segment_duration_field(
        duration: Union[SegmentStringDuration, int, float, str, None]
    ):
        """
        Validate that the given 'duration' is valid for a
        Segment.
        """
        return BuilderValidator._validate_component_duration_field(
            duration,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_enhancement_duration_field(
        duration: Union[EnhancementStringDuration, int, float, str, None]
    ):
        """
        Validate that the given 'duration' is valid for an
        Enhancement.
        """
        return BuilderValidator._validate_component_duration_field(
            duration,
            Component.ENHANCEMENT
        )
    
    @staticmethod
    def validate_shortcode_duration_field(
        duration: Union[ShortcodeStringDuration, int, float, str, None]
    ):
        """
        Validate that the given 'duration' is valid for a
        Shortcode.
        """
        return BuilderValidator._validate_component_duration_field(
            duration,
            Component.SHORTCODE
        )

    @staticmethod
    def _validate_component_duration_field(
        duration: Union[SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration, int, float, str],
        component: Component
    ):
        """
        Validate that the provided 'duration' is valid for
        the given 'component'.
        """
        component = Component.to_enum(component)

        return component.get_duration(duration)
    
    # DURATION FOR TYPE below
    def validate_segment_duration_for_type(
        duration: Union[SegmentStringDuration, int, float, str],
        type: Union[SegmentType, str]
    ):
        """
        Validate if the provided 'duration' is accepted by
        the also given 'type' for a Segment component.
        """
        return BuilderValidator._validate_component_duration_for_type(
            duration,
            type,
            Component.SEGMENT
        )
    
    def validate_enhancement_duration_for_type(
        duration: Union[EnhancementStringDuration, int, float, str],
        type: Union[EnhancementType, str]
    ):
        """
        Validate if the provided 'duration' is accepted by
        the also given 'type' for an Enhancement component.
        """
        return BuilderValidator._validate_component_duration_for_type(
            duration,
            type,
            Component.ENHANCEMENT
        )
    
    def validate_shortcode_duration_for_type(
        duration: Union[ShortcodeStringDuration, int, float, str],
        type: Union[ShortcodeType, str]
    ):
        """
        Validate if the provided 'duration' is accepted by
        the also given 'type' for a Shortcode component.
        """
        return BuilderValidator._validate_component_duration_for_type(
            duration,
            type,
            Component.SHORTCODE
        )

    @staticmethod
    def _validate_component_duration_for_type(
        duration: Union[SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration, int, float, str],
        type: Union[SegmentType, EnhancementType, ShortcodeType, str],
        component: Component
    ):
        """
        Validate if the provided 'duration' is accepted by
        the also given 'type' for the also provided
        'component'.
        """
        component = Component.to_enum(component)

        if not component.is_duration_accepted_for_type(duration, type):
            type = (
                type
                if PythonValidator.is_string(type) else
                type.value
            )

            raise Exception(f'The "{type}" type does not accept the provided "{duration}" duration.')

    # START below
    @staticmethod
    def validate_segment_start_field(
        start: Union[int, float, str, None]
    ):
        """
        Validate that the provided 'start' is valid
        for a Segment component.
        """
        return BuilderValidator._validate_component_start_field(
            start,
            Component.SEGMENT
        )
    
    @staticmethod
    def validate_enhancement_start_field(
        start: Union[int, float, str, None]
    ):
        """
        Validate that the provided 'start' is valid
        for an Enhancement component.
        """
        return BuilderValidator._validate_component_start_field(
            start,
            Component.ENHANCEMENT
        )
    
    @staticmethod
    def validate_shortcode_start_field(
        start: Union[int, float, str, None]
    ):
        """
        Validate that the provided 'start' is valid
        for a Shortcode component.
        """
        return BuilderValidator._validate_component_start_field(
            start,
            Component.SHORTCODE
        )

    @staticmethod
    def _validate_component_start_field(
        start: Union[int, float, str, None],
        component: Component
    ):
        """
        Validate that the provided 'start' is valid
        for the given 'component'.
        """
        component = Component.to_enum(component)

        return component.get_start(start)

class SegmentJsonValidator:
    """
    Class to wrap the validation of a Segment
    that is still a raw json.
    """

    @staticmethod
    def validate(
        segment: dict
    ):
        """
        Validate a raw segment that has been read from
        a json file to check if it fits all the expected
        conditions, raising an Exception if not.
        """
        # 1. Validate that contains all the expected fields
        validate_segment_has_expected_fields(segment)

        # 2. Validate that the 'type' is valid
        validate_segment_type_is_valid(segment)

        # 3. Validate that 'text' has no shortcodes
        validate_segment_text_has_no_shortcodes(segment)

        # 4. Validate that 'text_to_narrate' doesn't have
        # invalid shortcodes
        validate_segment_text_to_narrate_has_no_invalid_shortcodes(segment)

        # 5. Validate that 'duration' is a valid string or
        # a positive numeric value
        validate_segment_duration_is_valid_string_or_positive_number(segment)

        # 6. Validate that 'duration' is FILE_DURATION for
        # a valid type
        validate_segment_duration_is_valid_for_type(segment)

        # 7. Validate if the type has the mandatory fields
        validate_segment_has_extra_params_needed(segment)

        # 8. Validate that the segment enhancements are ok
        for enhancement in segment.get(SegmentField.ENHANCEMENTS.value, []):
            EnhancementJsonValidator.validate(enhancement)

        # 9. Validate segment mandatory conditions are met
        validate_segment_mets_mandatory_conditions(segment)

class EnhancementJsonValidator:
    """
    Class to wrap the validation of a Segment
    that is still a raw json.
    """

    @staticmethod
    def validate(
        enhancement: dict
    ):
        """
        Validate a raw enhancement that has been read
        from a json file to check if it fits all the
        expected conditions, raising an Exception if
        not.
        """
        # 1. Validate that contains all the expected fields
        validate_enhancement_has_all_fields(enhancement)

        # 2. Validate that the 'type' is valid
        validate_enhancement_type_is_valid(enhancement)

        # 3. Validate that 'text' has no shortcodes
        validate_enhancement_text_has_no_shortcodes(enhancement)

        # 4. Validate that 'text_to_narrate' doesn't have
        # invalid shortcodes
        validate_enhancement_text_to_narrate_has_no_invalid_shortcodes(enhancement)

        # 5. Validate that 'duration' is a valid string or
        # a positive numeric value
        validate_enhancement_duration_is_valid_string_or_positive_number(enhancement)

        # 6. Validate that 'duration' is FILE_DURATION for
        # a valid type
        validate_enhancement_duration_is_valid_for_type(enhancement)

        # 7. Validate that 'mode' is valid
        validate_enhancement_mode_is_valid_for_type(enhancement)

        # 8. Validate all the mandatory conditions are met
        Configuration.get_configuration_by_type(
            enhancement.get(EnhancementField.TYPE, None)
        ).validate_component_mandatory_conditions(enhancement)


# Validation methods below
def validate_enhancement_has_all_fields(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' contains
    all the expected keys, which are all the ones
    available through the EnhancementField Enum
    class, and raises an Exception if not.
    """
    BuilderValidator.validate_enhancement_has_expected_fields(enhancement)
    
def validate_enhancement_type_is_valid(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has a valid
    type or raises an Exception if not.
    """
    EnhancementType.to_enum(enhancement.get(EnhancementField.TYPE.value, None))

def validate_enhancement_text_has_no_shortcodes(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has any 
    shortcode in its 'text' field and raises
    an Exception if so.
    """
    try:
        empty_shortcode_parser.parse(enhancement.get(EnhancementField.TEXT.value, ''))
    except Exception:
        raise Exception(f'The "enhancement" has some shortcodes in its "{EnhancementField.TEXT.value}" field and this is not allowed.')
    
def validate_enhancement_text_to_narrate_has_no_invalid_shortcodes(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has any
    invalid shortcode in its 'text_to_narrate'
    and raises an Exception if so.
    """
    try:
        # TODO: This has to be our general shortcode parser
        # TODO: I just faked it by now
        shortcode_parser = None
        shortcode_parser.parse(enhancement.get(EnhancementField.TEXT_TO_NARRATE.value, ''))
    except Exception:
        raise Exception(f'The "enhancement" has some invalid shortcodes in its "{EnhancementField.TEXT_TO_NARRATE.value}" field. Please, check the valid shortcodes.')
    
def validate_enhancement_duration_is_valid_string_or_positive_number(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has a 'duration'
    field that is a valid string or a positive 
    number and raises an Exception if not.
    """
    BuilderValidator.validate_enhancement_duration_field(
        enhancement.get(EnhancementField.DURATION.value, None)
    )

def validate_enhancement_duration_is_valid_for_type(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has a 'duration'
    field that is a valid string for its type or a
    positive number and raises an Exception if not.
    """
    BuilderValidator.validate_enhancement_duration_for_type(
        enhancement.get(EnhancementField.DURATION.value, None),
        enhancement.get(EnhancementField.TYPE.value, None)
    )
    
def validate_enhancement_mode_is_valid_for_type(
    enhancement: dict
):
    """
    Check if the provided 'enhancement' has a 'mode' 
    field that is valid for its type.
    """
    BuilderValidator.validate_enhancement_mode_for_type(
        enhancement.get(EnhancementField.MODE.value, None),
        enhancement.get(EnhancementField.TYPE.value, None)
    )

def validate_segment_has_expected_fields(
    segment: dict
):
    """
    Check if the provided 'segment' contains all
    the expected keys, which are all the ones
    available through the SegmentField Enum class,
    and raises an Exception if not.
    """
    BuilderValidator.validate_segment_has_expected_fields(
        segment
    )
    
def validate_segment_type_is_valid(
    segment: dict
):
    """
    Check if the provided 'segment' has a valid
    type or raises an Exception if not.
    """
    SegmentType.to_enum(segment.get(SegmentField.TYPE.value, None))

def validate_segment_text_has_no_shortcodes(
    segment: dict
):
    """
    Check if the provided 'segment' has any 
    shortcode in its 'text' field and raises
    an Exception if so.
    """
    try:
        empty_shortcode_parser.parse(segment.get(SegmentField.TEXT.value, ''))
    except Exception:
        raise Exception(f'The "segment" has some shortcodes in its "{SegmentField.TEXT.value}" field and this is not allowed.')
    
def validate_segment_text_to_narrate_has_no_invalid_shortcodes(
    segment: dict
):
    """
    Check if the provided 'segment' has any
    invalid shortcode in its 'text_to_narrate'
    and raises an Exception if so.
    """
    try:
        shortcode_parser.parse(segment.get(SegmentField.TEXT_TO_NARRATE.value, ''))
    except Exception:
        raise Exception(f'The "segment" has some invalid shortcodes in its "{SegmentField.TEXT_TO_NARRATE.value}" field. Please, check the valid shortcodes.')
    
def validate_segment_duration_is_valid_string_or_positive_number(
    segment: dict
):
    """
    Check if the provided 'segment' has a 'duration'
    field that is a valid string or a positive 
    number and raises an Exception if not.
    """
    BuilderValidator.validate_segment_duration_field(
        segment.get(SegmentField.DURATION.value, None)
    )

def validate_segment_duration_is_valid_for_type(
    segment: dict
):
    """
    Check if the provided 'segment' has a 'duration'
    field that is a valid string for its component
    type or raises an Exception if not.
    """
    BuilderValidator.validate_segment_duration_for_type(
        segment.get(SegmentField.DURATION.value, None),
        type = segment.get(SegmentField.TYPE.value, None)
    )
    
def validate_segment_has_extra_params_needed(
    segment: dict
):
    """
    Check if the provided 'segment' has the extra
    parameters that are needed according to its
    type and keywords (premades or text premades
    need extra parameters to be able to be built),
    or raises an Exception if not.
    """
    # TODO: Validate, if premade or effect, that 'extra_params' has
    # needed fields
    keywords = segment.get(SegmentField.KEYWORDS.value, None)
    if type == SegmentType.PREMADE.value:
        # TODO: This below was prepared for extra_params, I think
        # I don't have to ignore anything here... but we were
        # avoiding 'duration' because we obtain it from main fields
        if not is_element_valid_for_method(
            method = enum_name_to_class(keywords, Premade).generate,
            element = segment,
            #parameters_to_ignore = ['duration'],
            parameters_strictly_from_element = ['duration']
        ):
            # TODO: I don't tell anything about the parameters needed
            raise Exception('Some parameters are missing...')
    elif type == SegmentType.TEXT.value:
        # TODO: This below was prepared for extra_params, I think
        # I don't have to ignore anything here... but we were
        # avoiding 'text' and 'duration' because we obtain them
        # from main fields
        if not is_element_valid_for_method(
            method = enum_name_to_class(keywords, TextPremade).generate,
            element = segment,
            #parameters_to_ignore = ['output_filename', 'duration', 'text']
            parameters_to_ignore = ['output_filename'],
            parameters_strictly_from_element = ['duration', 'text']
        ):
            # TODO: I don't tell anything about the parameters needed
            raise Exception('Some parameters are missing...')
    # TODO: Validate for another types

def validate_segment_mets_mandatory_conditions(
    segment: dict
):
    """
    Check if the provided 'segment' mets all the
    mandatory conditions, that are those starting
    with 'do_' in the configuration dict and that
    have a True value, or raises an Exception if
    those mandatory conditions are not met.
    """
    Configuration.get_configuration_by_type(
        segment.get(SegmentField.TYPE.value, None)
    )().validate_component_mandatory_conditions(segment)
