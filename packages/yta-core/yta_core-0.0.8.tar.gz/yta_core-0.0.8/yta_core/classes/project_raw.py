"""
A project that has been read from a file and
all its data is raw.
"""
from yta_core.classes.project_validated import ProjectValidated
from yta_core.classes.segment_json import SegmentJson
from yta_core.classes.enhancement_json import EnhancementJson
from yta_core.validation import SegmentJsonValidator
from yta_core.enums.status import ProjectStatus, SegmentStatus
from yta_core.enums.field import ProjectField, SegmentField, EnhancementField
from yta_core.enums.string_duration import SegmentStringDuration, EnhancementStringDuration
from yta_core.shortcodes.parser import shortcode_parser
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
            SegmentJsonValidator.validate(segment)

        return json



