from yta_core.enums.type import SegmentType, EnhancementType, ShortcodeType
from yta_core.enums.string_duration import SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration
from yta_core.enums.mode import SegmentMode, EnhancementMode, ShortcodeMode
from yta_core.enums.start import SegmentStart, EnhancementStart, ShortcodeStart
from yta_core.configuration import Configuration, ConfigurationAsSegment, ConfigurationAsEnhancement, ConfigurationAsShortcode
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.validator.number import NumberValidator
from typing import Union


class Component(Enum):
    """
    Enum class to indicate the different componentes 
    we have in the application.
    """

    SEGMENT = 'segment'
    ENHANCEMENT = 'enhancement'
    SHORTCODE = 'shortcode'

    def get_type(
        self,
        type: Union[SegmentType, EnhancementType, ShortcodeType, str]
    ) -> Union[SegmentType, EnhancementType, ShortcodeType]:
        """
        Get the 'type' parsed as a Enum class for this
        Component, or raises an Exception if invalid.
        """
        if (
            not PythonValidator.is_string(type) and
            not PythonValidator.is_instance(type, [SegmentType, EnhancementType, ShortcodeType])
        ):
            raise Exception('The provided "type" is not an accepted value.')

        return {
            Component.SEGMENT: lambda type: SegmentType.to_enum(type),
            Component.ENHANCEMENT: lambda type: EnhancementType.to_enum(type),
            Component.SHORTCODE: lambda type: ShortcodeType.to_enum(type)
        }[self](type)

    def get_duration(
        self,
        duration: Union[SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration, int, float, str]
    ) -> Union[SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration, int, float, str]:
        """
        Get the 'duration' parsed as a Enum class (if a
        valid string for that) or as it is (if valid) for
        this Component, or raises an Exception if invalid.
        """
        if (
            duration is None or
            (
                not PythonValidator.is_string(duration) and
                not NumberValidator.is_positive_number(duration, do_include_zero = False) and
                not PythonValidator.is_instance(duration, SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration)
            )
        ):
            raise Exception('The provided "duration" is not an accepted value.')
        
        return (
            {
                Component.SEGMENT: lambda duration: SegmentStringDuration.to_enum(duration),
                Component.ENHANCEMENT: lambda duration: EnhancementStringDuration.to_enum(duration),
                Component.SHORTCODE: lambda duration: ShortcodeStringDuration.to_enum(duration)
            }[self](duration)
            if not NumberValidator.is_positive_number(duration) else
            duration
        )
    
    def get_start(
        self,
        start: Union[SegmentStart, EnhancementStart, ShortcodeStart, int, float, str]
    ) -> Union[SegmentStart, EnhancementStart, ShortcodeStart]:
        """
        Get the 'start' parsed as a Enum class (if a valid
        string for that) or as it is (if valid) for this
        Component, or raises an Exception if invalid.
        """
        # TODO: I think we do not accept None as 'start'
        if (
            start is None or
            (
                not PythonValidator.is_string(start) and
                not NumberValidator.is_positive_number(start, do_include_zero = False) and
                not PythonValidator.is_instance(start, SegmentStart, EnhancementStart, ShortcodeStart)
            )
        ):
            raise Exception('The provided "duration" is not an accepted value.')
        
        return (
            {
                Component.SEGMENT: SegmentStart.to_enum(start),
                Component.ENHANCEMENT: EnhancementStart.to_enum(start),
                Component.SHORTCODE: ShortcodeStart.to_enum(start)
            }[self](start)
            if not NumberValidator.is_positive_number(start) else
            start
        )
    
    def get_mode(
        self,
        mode: Union[SegmentMode, EnhancementMode, ShortcodeMode, str],
    ) -> Union[SegmentMode, EnhancementMode, ShortcodeMode]:
        """
        Get the 'mode' parsed as a Enum class for this
        Component, or raises an Exception if invalid.
        """
        if (
            not PythonValidator.is_string(mode) and
            not PythonValidator.is_instance(mode, SegmentMode, EnhancementMode, ShortcodeMode)
        ):
            raise Exception('The provided "mode" is not an accepted value.')
        
        return {
            Component.SEGMENT: lambda mode: SegmentMode.to_enum(mode),
            Component.ENHANCEMENT: lambda mode: EnhancementMode.to_enum(mode),
            Component.SHORTCODE: lambda mode: ShortcodeMode.to_enum(mode)
        }[self](mode)

    def get_config_for_type(
        self,
        type: Union[SegmentType, EnhancementType, ShortcodeType, str]
    ) -> Union[ConfigurationAsSegment, ConfigurationAsEnhancement, ConfigurationAsShortcode]:
        """
        Get the configuration for this component for the
        specific provided 'type'.
        """
        return {
            Component.SEGMENT: lambda type: Configuration.get_configuration_by_type(type)._config_as_segment,
            Component.ENHANCEMENT: lambda type: Configuration.get_configuration_by_type(type)._config_as_enhancement,
            Component.SHORTCODE: lambda type: Configuration.get_configuration_by_type(type)._config_as_shortcode
        }[self](self.get_type(type))

    def is_mode_accepted_for_type(
        self,
        mode: Union[SegmentMode, EnhancementMode, ShortcodeMode, str, None],
        type: Union[SegmentType, EnhancementType, ShortcodeType, str]
    ) -> bool:
        """
        Check if the provided 'mode' is accepted for the
        given 'type' in this component.
        """
        type = self.get_type(type)
        mode = self.get_mode(mode)

        return mode in self.get_config_for_type(type).modes

    def is_duration_accepted_for_type(
        self,
        duration: Union[SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration, int, float, str],
        type: Union[SegmentType, EnhancementType, ShortcodeType, str]
    ) -> bool:
        """
        Check if the provided 'duration' is accepted for
        the given 'type' in this component.
        """
        type = self.get_type(type)
        duration = self.get_duration(duration)
        config_for_type = self.get_config_for_type(type)

        string_durations = (
            config_for_type.string_durations
            if config_for_type.string_durations is not None else
            []
        )

        return (
            NumberValidator.is_positive_number(duration) or
            duration in string_durations
        )