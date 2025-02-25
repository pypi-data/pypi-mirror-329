"""
The edition manual is a real concept translated
into programming.

Think about a content creator that always edits
his videos in the same way (him or his paid
editor). The editor has a bank of memes, sounds,
images, and tries to do the same in all the videos
he edits. This is using your edition guideline.
Applying your edition manual. And that's the idea
we want to build here.

When you are editing, you put some images when some
concept is mentioned, or maybe a sound is played
when you say a joke. Or, simply, a censorship sound
is added when a bad word is said.

All this can be automated by writting this edition
manual and telling the software how and when you
want the clip to be edited with any resource you
want. You maybe want an effect, a sound, a sticker
image, some specific video clip played overlay
during X seconds. All this is what you can do here.

Here is an example of an Edition Manual based on
football topic:

'terms': {
    'Lionel Messi': {
        'mode': 'exact',
        'context': 'generic',
        'enhancements': [
            {
                'type': 'sticker',
                'keywords': 'lionel messi portrait',
                'url': '',
                'filename': '',
                'mode': 'overlay'
            }
        ]
    },
    'Cristiano Ronaldo': {
        'mode': 'exact',
        'context': 'generic',
        'enhancements': [
            {
                'type': 'sticker',
                'keywords': 'cristiano ronaldo portrait',
                'url': '',
                'filename': '',
                'mode': 'overlay'
            }
        ]
    }
}
"""
from yta_core.edition_manual.term import EditionManualTerm
from yta_audio.voice.transcription.objects import AudioTranscription
from yta_general_utils.file.reader import FileReader
from yta_general_utils.programming.validator.parameter import ParameterValidator


class EditionManual:
    """
    Class to encapsulate all the terms to be 
    used to edit a video in the way the user
    expects with this configuration.

    This EditionManual will hold a lof of terms
    that will be transformed into effects,
    videos, texts and any other kind of elements
    supporting the raw video according to the
    specifications of these terms.
    """
    
    terms: list[EditionManualTerm] = None
    """
    The list containing all the terms that
    belongs to this Edition Manual and are
    applicable here.
    """

    def __init__(
        self,
        terms: list[EditionManualTerm]
    ):
        # TODO: We need an ID or maybe we can use
        # the json as the identifier (as we do with
        # the projects)
        self.terms = terms

    @staticmethod
    def init_from_file(
        filename: str
    ) -> 'EditionManual':
        """
        Initialize an Edition Manual from the
        given file 'filename' that must have a
        valid structure.
        """
        ParameterValidator.validate_mandatory_string('filename', filename, do_accept_empty = False)

        file_content = FileReader.read_json(filename)
        # Check if file is valid
        if file_content.get('terms', None) is None:
            raise Exception(f'No "terms" field found in the provided json filename {filename}.')

        return EditionManual.init_from_dict(
            file_content['terms']
        )

    @staticmethod
    def init_from_dict(
        terms: dict
    ) -> 'EditionManual':
        """
        Initialize an EditionManual instance with
        each of the provided 'terms' being
        instantiated as EditionManualTerms.
        """
        return EditionManual([
            # This method will raise an Exception
            # if some term is not valid
            EditionManualTerm.init_from_dict(
                key,
                content
            )
            for key, content in terms.items()
        ])

    def apply(
        self,
        transcription: AudioTranscription
    ) -> list:
        """
        Apply this edition manual to the given
        'transcription' so we are able to find the
        terms we are looking for and the indexes
        in which those terms are found, that will
        be converted to the time moments to be
        able to place the improvements in the
        moment they are expected to be applied.
        """
        return [
            item
            for term in self.terms
            for item in term.search(transcription)
        ]