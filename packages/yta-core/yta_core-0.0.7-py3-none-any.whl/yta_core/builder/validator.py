"""
Module to centralize the validation of the different
type of components we have in the system: Segment,
Enhancement, Shortcode...
"""
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