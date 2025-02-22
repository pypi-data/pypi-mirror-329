"""
A project that has been read from a file and
all its data is raw.
"""
from yta_core.classes.project_validated import ProjectValidated
from yta_core.classes.segment_json import SegmentJson
from yta_core.classes.enhancement_json import EnhancementJson
from yta_core.enums.status import ProjectStatus, SegmentStatus
from yta_core.enums.field import ProjectField, SegmentField, EnhancementField
from yta_core.enums.type import SegmentType, EnhancementType
from yta_core.enums.string_duration import SegmentStringDuration, EnhancementStringDuration
from yta_core.shortcodes.parser import shortcode_parser, empty_shortcode_parser
from yta_core.builder.enums import Premade, TextPremade
from yta_core.builder.utils import enum_name_to_class
from yta_core.builder import is_element_valid_for_method
from yta_core.configuration import Configuration
from yta_core.builder.validator import BuilderValidator
from yta_general_utils.file.checker import FileValidator
from yta_general_utils.file.reader import FileReader
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.programming.validator import PythonValidator
from datetime import datetime
from dataclasses import dataclass

import copy


@dataclass
class ProjectRaw:
    """
    @dataclass
    Class to represent a raw project that has
    been read from a .json file and has to be
    validated to pass to the next building step.

    Once its been validated it will turn into 
    a ProjectValidated instance.
    """

    json: dict
    """
    The project raw json information as a dict.
    """

    @property
    def as_project_validated(
        self
    ) -> ProjectValidated:
        """
        The project but transformed into a
        ProjectValidated instance.
        """
        if not hasattr(self, '_for_database'):
            data = ProjectValidated(
                ProjectStatus.TO_START.value,
                copy.deepcopy(self.json),
                []
            )

            # TODO: This shortcode parser must be instantiated once, and this is
            # being instantiated twice in this file
            segments = []
            for segment in self.json['segments']:
                segment_data = SegmentJson()

                # We only need SegmentFields because it is being
                # read from a file, so no building process yet
                for field in SegmentField.get_all_values():
                    setattr(segment_data, field, segment[field])

                # TODO: Remove this below when working, please
                # TODO: What about 'type', 'url', 'text', etc (?)
                # type
                # url
                # text
                # keywords
                # filename
                # audio_narration_filename
                # music
                # voice
                # enhancements (?)
                # extra_params (?)

                if segment.get(SegmentField.TEXT_TO_NARRATE.value, ''):
                    # Process shortcodes in 'text_to_narrate'
                    shortcode_parser.parse(segment[SegmentField.TEXT_TO_NARRATE.value])
                    segment_data.text_to_narrate_sanitized_without_shortcodes = shortcode_parser.text_sanitized_without_shortcodes
                    segment_data.text_to_narrate_with_simplified_shortcodes = shortcode_parser.text_sanitized_with_simplified_shortcodes
                    segment_data.text_to_narrate_sanitized = shortcode_parser.text_sanitized

                # Transform string duration into its numeric value
                duration = segment.get(SegmentField.DURATION.value, None)
                if (
                    duration is not None and
                    PythonValidator.is_string(duration)
                ):
                    segment_data.duration = SegmentStringDuration.to_numeric_value(duration)
                        
                segment_data.status = SegmentStatus.TO_START.value
                segment_data.created_at = datetime.now()

                for enhancement in segment.get(SegmentField.ENHANCEMENTS.value, []):
                    enhancement_data = EnhancementJson()

                    # We only need EnhancementFields because it is
                    # being read from a file, so no building process yet
                    for field in EnhancementField.get_all_values():
                        setattr(enhancement_data, field, enhancement[field])

                    if enhancement.get(EnhancementField.TEXT_TO_NARRATE.value, ''):
                        # Process shortcodes in 'text_to_narrate'
                        shortcode_parser.parse(enhancement[EnhancementField.TEXT_TO_NARRATE.value])
                        enhancement_data.text_to_narrate_sanitized_without_shortcodes = shortcode_parser.text_sanitized_without_shortcodes
                        enhancement_data.text_to_narrate_with_simplified_shortcodes = shortcode_parser.text_sanitized_with_simplified_shortcodes
                        enhancement_data.text_to_narrate_sanitized = shortcode_parser.text_sanitized

                    # Manually handle string duration
                    enhancement_duration = enhancement.get('duration', None)
                    if (
                        enhancement_duration is not None and
                        PythonValidator.is_string(enhancement_duration)
                    ):
                        enhancement_data.duration = EnhancementStringDuration.to_numeric_value(enhancement_duration)

                    enhancement_data.status = SegmentStatus.TO_START.value
                    enhancement_data.created_at = datetime.now()

                    # Store that enhancement data
                    segment_data.enhancements.append(enhancement_data)
                segments.append(segment_data)
            data.segments = segments

            self._for_database = data

        return self._for_database
    
    def __init__(
        self,
        json: dict
    ):
        ParameterValidator.validate_mandatory_dict('json', json)

        # If project is invalid it will never be an instance
        # of it
        self.json = ProjectRaw.validate_project_json_from_file(json)

    @staticmethod
    def init_from_file(
        filename: str
    ) -> 'ProjectRaw':
        """
        Initializes a ProjectRaw instance reading the
        information from the given file 'filename'.
        """
        ParameterValidator.validate_mandatory_string('filename', filename, do_accept_empty = False)

        if not FileValidator.is_file(filename):
            raise Exception('The provided "filename" is not a valid filename.')

        return ProjectRaw(
            FileReader.read_json(filename)
        )
    
    @staticmethod
    def validate_project_json_from_file(
        json: dict
    ) -> dict:
        """
        Validate the 'json' that has been read from a file
        and raises an Exception if invalid. This method
        returns the same 'json' dict if valid.
        """
        ParameterValidator.validate_mandatory_dict('json', json)
        
        segments = json.get(ProjectField.SEGMENTS.value, None)
        if segments is None:
            raise Exception('The provided "json" dict does not contain a "segments" field.')
        
        # Lets validate the content of each segment
        for segment in segments:
            validate_segment(segment)

        return json

# TODO: These methods are here because they are
# related to a raw segment written into a json
# file, but the name is not clear out of this
# module context. Maybe use as staticmethod or
# create a ProjectRawValidator static class
# to wrap the methods
def validate_segment(
    segment: dict
):
    """
    Validate a raw segment that has been read from
    a json file to check if it fits all the expected
    conditions.
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
        validate_enhancement(enhancement)

    # 9. Validate segment mandatory conditions are met
    validate_segment_mets_mandatory_conditions(segment)

def validate_enhancement(
    enhancement: dict
):
    """
    Validate a raw enhancement, that belongs to
    a raw segment that has been read from a json
    file to check if it fits all the expected
    conditions.
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
