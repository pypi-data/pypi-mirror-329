from youtube_autonomous.experimental.enhancement.enhancement_element import EnhancementElement
from youtube_autonomous.elements.validator.element_validator import ElementValidator

from yta_core.configuration import Configuration
from yta_core.enums.component import Component
from yta_core.enums.start import ShortcodeStart
from yta_core.enums.field import ShortcodeField
from yta_core.enums.type import ShortcodeType
from yta_core.enums.mode import ShortcodeMode
from yta_core.enums.string_duration import ShortcodeStringDuration
from yta_shortcodes.tag_type import ShortcodeTagType
from yta_shortcodes.shortcode import YTAShortcode as BaseShortcode
from yta_audio.voice.transcription.objects import AudioTranscription
from typing import Union


LOWER_INDEX = -1
UPPER_INDEX = 99999

# TODO: Maybe inherit from YTAShortcode and
# refactor to implement the new things
class Shortcode(BaseShortcode):
    """
    Class that represent a shortcode detected in a text, containing 
    its attributes and values and also the content if block-scoped.
    """
    
    tag: ShortcodeType
    """
    The shortcode tag that represents and identifies
    it, determining the way it will be built and
    applied.
    """
    type: ShortcodeTagType
    """
    The type of the shortcode, that identifies it
    as a simple or a block shortcode.
    """
    _start: float
    _duration: float
    _keywords: str
    _filename: str
    _url: str
    _mode: ShortcodeMode
    context: any # TODO: Do I really need this (?)
    content: Union[str, None]
    """
    The text that is between the shortcode open and
    end tag and can include shortcodes. This
    parameter makes sense if the shortcode is a
    block-scoped shortcode and will be None if it is
    a simple-scoped one.
    """
    start_previous_word_index: Union[int, None]
    """
    The index of the word that is inmediately before
    the start tag of this shortcode. Could be None if
    the shortcode is just at the begining. This index
    is considered within the text empty of shortcodes.
    """
    end_previous_word_index: Union[int, None]
    """
    The index of the word that is inmediately before
    the end tag of this shortcode. It is None if the
    shortcode is a simple one. This index is 
    considered within the text empty of shortcodes.
    """

    def __init__(
        self,
        tag: ShortcodeType,
        type: ShortcodeTagType,
        context,
        content: Union[str, None],
        attributes: dict,
        start_previous_word_index: Union[int, None] = None,
        end_previous_word_index: Union[int, None] = None
    ):
        """
        The shortcode has a 'type' and could include some 'attributes' that
        are the parameters inside the brackets, that could also be simple or
        include an associated value. If it is a block-scoped shortcode, it
        will have some 'content' inside of it.
        """
        tag = ShortcodeType.to_enum(tag)
        type = ShortcodeTagType.to_enum(type)

        self.tag = tag
        self.type = type
        self.context = context
        self.content = content
        self.start_previous_word_index = start_previous_word_index
        self.end_previous_word_index = end_previous_word_index

        # Now the more special attributes
        # TODO: This was '.config_as_shortcode' previously
        self.config = Configuration.get_configuration_by_type(self.tag)._config_as_shortcode
        
        self.start = attributes.get(ShortcodeField.START.value, None)
        self.duration = attributes.get(ShortcodeField.DURATION.value, None)
        self.keywords = attributes.get(ShortcodeField.KEYWORDS.value, '')
        self.filename = attributes.get(ShortcodeField.FILENAME.value, '')
        self.url = attributes.get(ShortcodeField.URL.value, '')
        self.mode = attributes.get(ShortcodeField.MODE.value, None)

        # TODO: Should I treat these shortcodes as Enhancement so I need
        # to make the same checks (more specific that these ones below) (?)

        # TODO: I think I have to check if string durations
        # are valid according to the ConfigurationAsShortcode

        if (
            not self.keywords and
            not self.filename and
            not self.url
        ):
            raise Exception('No "keywords" nor "filename" nor "url" sources available.')

    @property
    def start(
        self
    ):
        """
        The time moment of the current segment in which this element is
        expected to be applied.
        """
        return self._start
    
    @start.setter
    def start(
        self,
        start: Union[ShortcodeStart, int, float, None]
    ):
        self.start = (
            {
                ShortcodeTagType.SIMPLE: ShortcodeStart.BETWEEN_WORDS,
                ShortcodeTagType.BLOCK: ShortcodeStart.START_OF_FIRST_SHORTCODE_CONTENT_WORD
            }[self.type]
            if start is None else
            Component.SHORTCODE.get_start(start)
        )

    @property
    def duration(
        self
    ):
        """
        The duration of the shortcode, that it is calculated according to the
        field or to its content.
        """
        return self._duration
    
    @duration.setter
    def duration(
        self,
        duration: Union[ShortcodeStringDuration, int, float, None]
    ):
        self._duration = (
            {
                ShortcodeTagType.SIMPLE: ShortcodeStringDuration.FILE_DURATION,
                ShortcodeTagType.BLOCK: ShortcodeStringDuration.SHORTCODE_CONTENT
            }[self.type]
            if duration is None else
            Component.SHORTCODE.get_duration(duration)
        )

    @property
    def mode(
        self
    ):
        return self._mode
    
    @mode.setter
    def mode(
        self,
        mode: Union[ShortcodeMode, str]
    ):
        mode = ShortcodeMode.to_enum(mode)

        if mode not in self.config.modes:
            raise Exception(f'The provided "{mode.value}" is not a valid mode for this shortcode type "{self.type.value}" and tag "{self.tag.value}".')

        self._mode = mode
    

    # TODO: This code below was using an experimental class
    # so it can no longer be like that
    # def to_enhancement_element(
    #     self,
    #     transcription: AudioTranscription
    # ):
    #     """
    #     Turns the current shortcode to an EnhancementElement by using
    #     the provided 'transcription' and using its words to set the
    #     actual 'start' and 'duration' fields according the narration.

    #     The provided 'transcription' could be not needed if the segment
    #     is not narrated and 'start' and 'duration' fields are manually
    #     set by the user in the shortcode.
    #     """
    #     if (
    #         self.type == ShortcodeTagType.SIMPLE and
    #         self.start_previous_word_index is None
    #     ):
    #         raise Exception(f'Found {ShortcodeTagType.SIMPLE.value} shortcode without "start_previous_word_index".')
        
    #     if (
    #         self.type == ShortcodeTagType.BLOCK and
    #         (self.start_previous_word_index is None or self.end_previous_word_index is None)
    #     ):
    #         raise Exception(f'Found {ShortcodeTagType.BLOCK.value} shortcode without "start_previous_word_index" or "end_previous_word_index".')
        
    #     self.calculate_start_and_duration(transcription)

    #     # TODO: Build it
    #     enhancement_element = EnhancementElement.get_class_from_type(self.tag)(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)

    #     # TODO: Remove this below if the code above is working
    #     # if self.tag == ShortcodeType.MEME:
    #     #     enhancement_element = MemeEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
    #     # elif self.tag == ShortcodeType.SOUND:
    #     #     enhancement_element = SoundEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
    #     # elif self.tag == ShortcodeType.IMAGE:
    #     #     enhancement_element = ImageEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
    #     # elif self.tag == ShortcodeType.STICKER:
    #     #     enhancement_element = StickerEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
    #     # elif self.tag == ShortcodeType.GREEN_SCREEN:
    #     #     enhancement_element = GreenscreenEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
    #     # elif self.tag == ShortcodeType.EFFECT:
    #     #     enhancement_element = EffectEnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)
    #     # else:
    #     #     raise Exception(f'No valid shortcode "{self.tag}" type provided.')
    #     #     # TODO: Implement the other EnhancementElements
    #     #     enhancement_element = EnhancementElement(self.tag, self.start, self.duration, self.keywords, self.url, self.filename, self.mode)

    #     return enhancement_element