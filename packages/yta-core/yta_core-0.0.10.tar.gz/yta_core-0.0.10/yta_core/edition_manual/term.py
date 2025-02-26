"""
A term is some text that we want to be matched
in a text so, when detected, we do something
to improve the content of the video (adding
an audio or video, applying some effect, etc.)
so we have to define the term and what we want
to be done.

Here is an example that would show an sticker
image of 'lionel messi portrait' when the 
exact term 'Lionel Messi' is found in the
audio transcription.

"Lionel Messi": {
    "mode": "exact",
    "context": "generic",
    "enhancements": [
        {
            "type": "sticker",
            "keywords": "lionel messi portrait",
            "url": "",
            "filename": "",
            "mode": "overlay"
        }
    ]
}
"""
from yta_core.classes.enhancement_json import EnhancementJson
from yta_core.enums.start import ShortcodeStart
from yta_core.edition_manual.enums import EditionManualTermContext, EditionManualTermField, EditionManualTermMode
from yta_audio.voice.transcription.objects import AudioTranscription
from yta_general_utils.text.finder import TextFinder
from yta_general_utils.file.reader import FileReader
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.programming.validator import PythonValidator
from typing import Union
from copy import copy

import json


class EditionManualTerm:
    """
    Class to describe the behaviour we want from
    this term when applying it over a video base.
    It can be transformed into an effect, a
    transition, a video and any other element 
    that will improve the video experience.

    More information:
    - https://www.notion.so/Diccionarios-de-mejora-155efcba8f0d44e0890b178effb3be84?pvs=4
    """

    term: str = None
    """
    The text of the term.
    """
    mode: Union[EditionManualTermMode, None] = None
    """
    The mode in which the term must be searched.
    """
    context: Union[EditionManualTermContext, str] = None
    """
    The context in which the term must be applied.

    This means, if this term is for a 'sport' context
    or similar, can only be used in that context.
    """
    _enhancements: list[EnhancementJson, dict] = None
    """
    The list of enhancements that must be applied when
    the term is found.
    """

    @property
    def as_dict(
        self
    ):
        """
        Get the instance as a dict in which there is
        only one unique key that is the 'term', and
        the values are its 'mode', 'context' and
        'enhancements' fields.
        """
        return {
            self.term: {
                EditionManualTermField.MODE.value: self.mode.value,
                EditionManualTermField.CONTEXT.value: self.context.value,
                # TODO: These enhancements have to be returned as dicts
                EditionManualTermField.ENHANCEMENTS.value: [
                    enhancement.as_dict
                    for enhancement in self.enhancements
                ]
            }
        }
    
    @property
    def as_json(
        self
    ):
        """
        Get the instance as a json.
        """
        return json.dumps(self.as_dict)

    @property
    def enhancements(
        self
    ):
        return self._enhancements
    
    @enhancements.setter
    def enhancements(
        self,
        enhancements: list[EnhancementJson, dict]
    ):
        # TODO: Make some checkings and improvements
        ParameterValidator.validate_mandatory_list_of_these_instances('enhancements', enhancements, [EnhancementJson, dict])

        # These enhancements should have been validated before when
        # the EditionManual is accepted, so now we consider them as
        # valids

        # Here 'enhancements' are only dicts

        # # We turn dicts to EnhancementElement if necessary
        # obj_enhancements = []
        # for enhancement in enhancements:
        #     if not isinstance(enhancement, EnhancementElement) and not issubclass(enhancement.__class__, EnhancementElement):
        #         obj_enhancements.append(EnhancementElement.get_class_from_type(enhancement['type'])(enhancement['type'], EnhancementElementStart.START_OF_FIRST_SHORTCODE_CONTENT_WORD, EnhancementElementDuration.SHORTCODE_CONTENT, enhancement['keywords'], enhancement.get('url', ''), enhancement.get('filename', ''), enhancement['mode']))
        #     else:
        #         obj_enhancements.append(enhancement)

        self._enhancements = enhancements

    def __init__(
        self,
        term: str,
        mode: Union[EditionManualTermMode, str],
        context: Union[EditionManualTermContext, str],
        enhancements: list[dict]
    ):
        mode = EditionManualTermMode.to_enum(mode)
        context = EditionManualTermContext.to_enum(context)

        self.term = term
        self.mode = mode
        self.context = context
        self.enhancements = enhancements

    @staticmethod
    def init_from_dict(
        term_key: str,
        term_content: dict
    ):
        """
        Initialize an instance from the given
        'term_key' and 'term_content'. The
        'term_content' must have the expected
        structure and the values must be valid
        for our system.

        An example would be:
        - term_key = 'Lionel Messi'
        - term_content = {
            'mode': 'inline',
            'context': 'any',
            'enhancements': []
        }
        """
        ParameterValidator.validate_mandatory_string('term_key', term_key, do_accept_empty = False)
        EditionManualTerm.validate(term_content)
        
        return EditionManualTerm(
            term = term_key,
            mode = term_content[EditionManualTermField.MODE.value],
            context = term_content[EditionManualTermField.CONTEXT.value],
            enhancements = term_content[EditionManualTermField.ENHANCEMENTS.value]
        )
    
    @staticmethod
    def validate(
        term_content: dict
    ):
        """
        Check that the provided 'term_content' has the
        mandatory attributes and that the values are
        valid as if it was an Enhancement written in the
        'guion' of a video.

        The 'term_content' must be the content associated
        to the term including not the term key.
        """
        all_mandatory_fields = EditionManualTermField.get_all_values()

        if (
            not PythonValidator.do_dict_has_keys(term_content, all_mandatory_fields) or
            len(term_content) != 3
        ):
            raise Exception(f'The "term_content" parameter provided must have only the {len(all_mandatory_fields)} fields we accept: {", ".join(all_mandatory_fields)}.')
        
        EditionManualTermMode.to_enum(term_content[EditionManualTermField.MODE.value])
        EditionManualTermContext.to_enum(term_content[EditionManualTermField.CONTEXT.value])

        enhancements = term_content[EditionManualTermField.ENHANCEMENTS.value]
        for enhancement in enhancements:
            # TODO: Validate enhancement structure as if 
            # it were in the 'guion' definition
            #EnhancementJson.validate(enhancement)
            pass

    # TODO: Maybe apply return type and a @dataclass (?)
    def search(
        self,
        transcription: AudioTranscription
    ):
        """
        Searches the term in the provided 'transcription' text
        and, if found, returns the corresponding Enhancements
        with the processed duration (if it is possible to
        process it).

        This method returns the list of enhancement elements
        that should be applied, according to the provided
        'transcription', as dict elements.
        """
        ParameterValidator.validate_mandatory_instance_of('transcription', transcription, AudioTranscription)

        terms_found = TextFinder.find_in_text(self.term, transcription.text, mode = self.mode)

        enhancements_found = []
        for term_found in terms_found:
            for term_enhancement in self.enhancements:
                # TODO: Handle 'enhancement' as @dataclass please
                # We will add some fields to the 'enhancement'
                enhancement_found = copy(term_enhancement)
                # TODO: If 'term' is just one word we cannot use this
                # strategy below
                if (
                    enhancement_found['start'] == ShortcodeStart.END_OF_FIRST_SHORTCODE_CONTENT_WORD.value and
                    term_found.start_index == term_found.end_index
                ):
                    enhancement_found['start'] = ShortcodeStart.START_OF_FIRST_SHORTCODE_CONTENT_WORD.value

                # Here we need to transform string 'start' and 'duration'
                # into their real numeric values
                start = None
                duration = None

                if enhancement_found['start'] == ShortcodeStart.START_OF_FIRST_SHORTCODE_CONTENT_WORD.value:
                    start = transcription[term_found.start_index]['start']
                    duration = transcription[term_found.end_index]['end'] - start
                elif enhancement_found['start'] == ShortcodeStart.MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD.value:
                    start = (transcription[term_found.start_index]['start'] + transcription[term_found.start_index]['end']) / 2
                    duration = (transcription[term_found.end_index]['start'] + transcription[term_found.end_index]['end']) / 2 - start
                elif enhancement_found['start'] == ShortcodeStart.END_OF_FIRST_SHORTCODE_CONTENT_WORD.value:
                    start = transcription[term_found.start_index]['end']
                    duration = start - transcription[term_found.end_index]['start']

                if (
                    start is None or
                    duration is None
                ):
                    raise Exception('Something went wrong when applying a EditionManualTerm.')

                enhancement_found['start'] = start
                enhancement_found['duration'] = duration
                
                # TODO: Should I turn this into a Enhancement object (?)
                # It is a dict right here
                enhancements_found.append(enhancement_found)

        return enhancements_found
