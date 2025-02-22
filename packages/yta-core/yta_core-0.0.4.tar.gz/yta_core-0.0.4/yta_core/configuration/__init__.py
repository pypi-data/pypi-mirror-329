"""
Module to include the different configurations for
the components we are able to build within our app
so we can set the parameters we expect to have or
the ones we need to be able to build each component
according to its type.

We have 2 different types of conditions:
- Mandatory conditions, that has to be met and if
not they raise an exception.
- Optional conditions, that can be met or can be
not, but don't raise an Exception if not met.

So, we have 4 different checkings we can do:
- If we must apply a mandatory condition and it
has to because it has the fields, lets apply it.
- If we must apply a mandatory condition and it
doesn't have the fields to apply it, raise an
Exception.
- If we can apply an optional condition and it
has to, lets apply it.
- If we can apply an optional condition and it
doesn't have the fields to, just ignore it.

Our mandatory conditions start with 'do_' and 
the optional ones with 'can_'.
"""
from yta_core.enums.type import SegmentType, EnhancementType, ShortcodeType, _Type
from yta_core.enums.mode import SegmentMode, EnhancementMode, ShortcodeMode
from yta_core.enums.string_duration import SegmentStringDuration, EnhancementStringDuration, ShortcodeStringDuration
from yta_core.configuration.condition.mandatory import DoNeedFilenameOrUrl, DoNeedKeywords, DoNeedNarration, DoNeedSpecificDuration, DoNeedText
from yta_general_utils.programming.decorators import classproperty
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.validator.number import NumberValidator
from yta_general_utils.programming.validator.parameter import ParameterValidator
from abc import ABCMeta
from typing import Union
from dataclasses import dataclass


@dataclass
class ConfigurationAsSegment:
    """
    @dataclass. The configuration of an element as a Segment. This
    must be used to check if the parameters provided 
    are valid for this element if acting as a Segment.
    """
    
    type: SegmentType
    modes: list[SegmentMode]
    """
    A list containing the Mode values that we accept
    in this configuration as a Segment component.
    """
    default_mode: SegmentMode
    string_durations: list[SegmentStringDuration]
    """
    A list containing the StringDuration values that
    we accept in this configuration as a Segment
    component.
    """

    def __init__(
        self,
        type: SegmentType,
        string_durations = None
    ):
        self.type = type,
        self.modes = None, # By now we don't accept modes
        self.default_mode = None # By now we don't accept modes
        self.string_durations = None 

    # TODO: Should we keep this below (?)
    @staticmethod
    def is_valid_type(
        segment_type: Union[str, SegmentType]
    ) -> bool:
        """
        Validates if the provided 'segment_type' is a valid name or 
        value of the registered and valid SegmentType enums. This
        method will return the Enum item if valid, or False if not.
        """
        return SegmentType.is_valid(segment_type)

    @staticmethod
    def is_valid_duration(
        duration: Union[float, int, str, SegmentStringDuration]
    ) -> bool:
        """
        Check if the provided 'duration' is valid for the
        current configuration.
        """
        return (
            SegmentStringDuration.is_valid(duration)
            if PythonValidator.is_string(duration) else
            NumberValidator.is_positive_number(duration)
        )
    # TODO: Should we keep this above (?)

class ConfigurationAsEnhancement:
    """
    The configuration of a component as an Enhancement.
    This must be used to check if the parameters provided 
    are valid for this component if acting as an Enhancement.
    """

    type: EnhancementType
    modes: list[EnhancementMode]
    """
    A list containing the Mode values that we accept
    in this configuration as an Enhancement component.
    """
    default_mode: EnhancementMode
    string_durations: list[EnhancementStringDuration]
    """
    A list containing the StringDuration values that
    we accept in this configuration as an Enhancement
    component.
    """

    def __init__(
        self,
        type: EnhancementType,
        modes: list[EnhancementMode],
        default_mode: EnhancementMode,
        string_durations: list[EnhancementStringDuration]
    ):
        self.type = type
        self.modes = modes
        self.default_mode = default_mode
        self.string_durations = string_durations

class ConfigurationAsShortcode:
    """
    The configuration of an element as a Shortcode.
    This must be used to check if the parameters provided 
    are valid for this element if acting as a Shortcode.
    """

    type: ShortcodeType
    modes: list[ShortcodeMode]
    default_mode: ShortcodeMode
    string_durations: list[ShortcodeStringDuration]
    """
    A list containing the StringDuration values that
    we accept in this configuration as a Shortcode
    component.
    """

    def __init__(
        self,
        type: EnhancementType,
        modes: list[ShortcodeMode],
        default_mode: ShortcodeMode,
        string_durations: list[ShortcodeStringDuration]
    ):
        self.type = type
        self.modes = modes
        self.default_mode = default_mode
        self.string_durations = string_durations

@dataclass
class Configuration(metaclass = ABCMeta):
    """
    Class to represent the configuration a 
    component can have according to its type.
    This must be used to check if the parameters
    provided are valid for this component.
    """
    
    _type: _Type

    _can_have_narration: bool
    """
    Can have a voice narration by setting the
    'text_to_narrate' and 'voice' fields, that
    will generate one, or by providing an
    'audio_narration_filename' that is a file
    containing a voice narration.
    """
    _do_need_voice_narration: bool
    """
    A voice narration is mandatory, so the
    'text_to_narrate' and 'voice' fields can
    be provided to generate a voice narration,
    or the 'audio_narration_filename', that is
    the file containing a voice narration.
    """
    _can_have_specific_duration: bool
    """
    The duration of this component can be set
    specifically so the element will long as
    much as the 'duration' field says.
    """
    _do_need_specific_duration: bool
    """
    The 'duration' field is mandatory in the
    situation in which the component cannot 
    have a voice narration or it can but the
    fields have not been set.
    """
    _can_have_text: bool
    """
    The 'text' field can be used to build the
    element in a specific way (determined by
    its type).
    """
    _do_need_text: bool
    """
    The 'text' field is mandatory so it must
    be set.
    """
    _can_have_filename: bool
    """
    The 'filename' field can be set to be used
    to load a file from that local stored
    filename.
    """
    _can_have_url: bool
    """
    The 'url' field can be set to be used to
    download a file from that url and use it.
    """
    _do_need_filename_or_url: bool
    """
    The 'url' or the 'filename' fields (one of
    both) are needed to be able to obtain the
    resource that need to be used to build the
    component. If both are given, the 'url' will
    be used.
    """
    _can_have_keywords: bool
    """
    The field 'keywords' can be set to use those
    keywords to look for the resource we need to
    build correctly the component (the way those
    'keywords' are used depends on the type).
    """
    _do_need_keywords: bool
    """
    The field 'keywords' is mandatory and must be
    set to be able to build the element.
    """
    _can_have_extra_parameters: bool
    """
    This field is a flag that let us know if the
    element can have some dynamic 'extra_params'
    that could be needed for the building process.
    For example, Premade and Text types could need
    extra parameters to be built ok.
    """

    _config_as_segment: Union[ConfigurationAsSegment, None]
    _config_as_enhancement: Union[ConfigurationAsEnhancement, None]
    _config_as_shortcode: Union[ConfigurationAsShortcode, None]

    @classproperty
    def type(cls):
        return cls._type

    @classproperty
    def can_have_narration(cls):
        return cls._can_have_narration
    
    @classproperty
    def do_need_voice_narration(cls):
        return cls._do_need_voice_narration
    
    @classproperty
    def can_have_specific_duration(cls):
        return cls._can_have_specific_duration
    
    @classproperty
    def do_need_specific_duration(cls):
        return cls._do_need_specific_duration
    
    @classproperty
    def can_have_text(cls):
        return cls._can_have_text
    
    @classproperty
    def do_need_text(cls):
        return cls._do_need_text
    
    @classproperty
    def can_have_filename(cls):
        return cls._can_have_filename
    
    @classproperty
    def can_have_url(cls):
        return cls._can_have_url
    
    @classproperty
    def do_need_filename_or_url(cls):
        return cls._do_need_filename_or_url

    @classproperty
    def can_have_keywords(cls):
        return cls._can_have_keywords
    
    @classproperty
    def do_need_keywords(cls):
        return cls._do_need_keywords
    
    @classproperty
    def can_have_extra_parameters(cls):
        return cls._can_have_extra_parameters
    
    @classproperty
    def config_as_segment(cls):
        return cls._config_as_segment
    
    @classproperty
    def can_be_segment(cls):
        return cls.config_as_segment is not None
    
    @classproperty
    def config_as_enhancement(cls):
        return cls._config_as_enhancement
    
    @classproperty
    def can_be_enhancement(cls):
        return cls.config_as_enhancement is not None
    
    @classproperty
    def config_as_shortcode(cls):
        return cls._config_as_shortcode
    
    @classproperty
    def can_be_shortcode(cls):
        return cls.config_as_shortcode is not None

    def __init__(
        self
    ):
        pass
    
    @staticmethod
    def get_configuration_by_type(
        type: Union[str, _Type]
        # TODO: Actually this is returning a subclass...
) -> Union['StockConfiguration', 'CustomStockConfiguration', 'AIImageConfiguration', 'ImageConfiguration', 'AIVideoConfiguration', 'VideoConfiguration', 'SoundConfiguration', 'YoutubeVideoConfiguration', 'TextConfiguration', 'MemeConfiguration', 'EffectConfiguration', 'PremadeConfiguration', 'GreenscreenConfiguration']:
        """
        Returns the configuration object that corresponds to
        the provided 'type' that need to be a valid type string
        or object.
        """
        type = (
            _Type.to_enum(type.value)
            if PythonValidator.is_enum(type) else
            _Type.to_enum(type)
        )

        return {
            _Type.STOCK: StockConfiguration,
            _Type.CUSTOM_STOCK: CustomStockConfiguration,
            _Type.AI_IMAGE: AIImageConfiguration,
            _Type.IMAGE: ImageConfiguration,
            _Type.AI_VIDEO: AIVideoConfiguration,
            _Type.VIDEO: VideoConfiguration,
            _Type.SOUND: SoundConfiguration,
            _Type.YOUTUBE_VIDEO: YoutubeVideoConfiguration,
            _Type.TEXT: TextConfiguration,
            _Type.MEME: MemeConfiguration,
            _Type.EFFECT: EffectConfiguration,
            _Type.PREMADE: PremadeConfiguration,
            _Type.GREENSCREEN: GreenscreenConfiguration
        }[type]

    def validate_component_mandatory_conditions(
        self,
        component: dict
    ):
        """
        Validate the mandatory conditions according to this
        configuration applied to the given 'component'. This
        will raise an Exception when some of those mandatory
        conditions is applicable and not met.
        """
        ParameterValidator.validate_mandatory_dict('component', component)

        if (
            self.do_need_voice_narration and
            not DoNeedNarration.is_satisfied(component)
        ):
            raise Exception('A voice narration is needed for this component and the necessary fields to build it are not set. The "audio_narration_filename" field, or the tuple "voice" and "text_to_narrate" fields are needed.')
        
        if (
            self.do_need_specific_duration and
            not DoNeedSpecificDuration.is_satisfied(component)
        ):
            raise Exception('A specific duration is needed for this component and the necessary fields to set it are not set. The "duration" field is needed, or a voice narration (built with "audio_narration_filename" or the tuple "voice" and "text_to_narrate" fields) are needed.')
        
        if (
            self.do_need_text and
            not DoNeedText.is_satisfied(component)
        ):
            raise Exception('A specific "text" field is needed and it is not set.')
        
        if (
            self.do_need_filename_or_url and
            not DoNeedFilenameOrUrl.is_satisfied(component)
        ):
            raise Exception('The "filename" field or the "url" field is needed for this component (at least one of them) and none are set.')
        
        if (
            self.do_need_keywords and
            not DoNeedKeywords.is_satisfied(component)
        ):
            raise Exception('The "keywords" field is needed for this component and it has not been set.')
        
    
@dataclass
class StockConfiguration(Configuration):
    """
    The 'Stock' element configuration, that defines if it can be used
    as a segment or as a enhancement (or both) and all the things it
    needs to work as expected.
    """
    _type = _Type.STOCK
    
    _can_have_narration = True
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = False
    _can_have_text: bool = False
    _do_need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _do_need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _do_need_keywords: bool = True
    _can_have_extra_parameters: bool = False

    _config_as_segment: ConfigurationAsSegment = ConfigurationAsSegment(
        type = SegmentType.STOCK,
    )
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.STOCK,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.STOCK,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass

@dataclass
class CustomStockConfiguration(Configuration):
    """
    The 'CustomStock' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.CUSTOM_STOCK
    
    _can_have_narration = True
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = False
    _can_have_text: bool = False
    _do_need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _do_need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _do_need_keywords: bool = True
    _can_have_extra_parameters: bool = False

    _config_as_segment: ConfigurationAsSegment = ConfigurationAsSegment(
        type = SegmentType.CUSTOM_STOCK,
    )
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.CUSTOM_STOCK,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.CUSTOM_STOCK,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass
    
@dataclass
class AIImageConfiguration(Configuration):
    """
    The 'AIImage' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.AI_IMAGE
    
    _can_have_narration = True
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = True
    _can_have_text: bool = False
    _do_need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _do_need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _do_need_keywords: bool = True
    _can_have_extra_parameters: bool = False

    _config_as_segment: ConfigurationAsSegment = ConfigurationAsSegment(
        type = SegmentType.AI_IMAGE,
    )
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.AI_IMAGE,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.AI_IMAGE,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass

@dataclass
class ImageConfiguration(Configuration):
    """
    The 'Image' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.IMAGE
    
    _can_have_narration = True
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = True
    _can_have_text: bool = False
    _do_need_text: bool = False
    _can_have_filename: bool = True
    _can_have_url: bool = True
    _do_need_filename_or_url: bool = True
    _can_have_keywords: bool = False
    _do_need_keywords: bool = False
    _can_have_extra_parameters: bool = False

    _config_as_segment: ConfigurationAsSegment = ConfigurationAsSegment(
        type = SegmentType.IMAGE,
    )
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.IMAGE,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.IMAGE,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass

@dataclass
class AIVideoConfiguration(Configuration):
    """
    The 'AIVideo' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.AI_VIDEO
    
    _can_have_narration = True
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = True
    _can_have_text: bool = False
    _do_need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _do_need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _do_need_keywords: bool = True
    _can_have_extra_parameters: bool = False

    _config_as_segment: ConfigurationAsSegment = ConfigurationAsSegment(
        type = SegmentType.AI_VIDEO,
    )
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.AI_VIDEO,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.AI_VIDEO,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass
    
@dataclass
class VideoConfiguration(Configuration):
    """
    The 'Video' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.VIDEO
    
    _can_have_narration = True
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = True
    _can_have_text: bool = False
    _do_need_text: bool = False
    _can_have_filename: bool = True
    _can_have_url: bool = True
    _do_need_filename_or_url: bool = True
    _can_have_keywords: bool = False
    _do_need_keywords: bool = False
    _can_have_extra_parameters: bool = False

    _config_as_segment: ConfigurationAsSegment = ConfigurationAsSegment(
        type = SegmentType.VIDEO,
    )
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.VIDEO,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.VIDEO,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass
    
@dataclass
class SoundConfiguration(Configuration):
    """
    The 'Sound' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.SOUND
    
    _can_have_narration = False
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = False
    _can_have_text: bool = False
    _do_need_text: bool = False
    _can_have_filename: bool = True
    _can_have_url: bool = True
    _do_need_filename_or_url: bool = True
    _can_have_keywords: bool = True
    _do_need_keywords: bool = False
    _can_have_extra_parameters: bool = False

    _config_as_segment: ConfigurationAsSegment = None
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.SOUND,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION, EnhancementStringDuration.FILE_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.SOUND,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT, ShortcodeStringDuration.FILE_DURATION]
    )

    def __init__(
        self
    ):
        pass

@dataclass
class YoutubeVideoConfiguration(Configuration):
    """
    The 'YoutubeVideo' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.YOUTUBE_VIDEO
    
    _can_have_narration = True
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = True
    _can_have_text: bool = False
    _do_need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = True
    _do_need_filename_or_url: bool = True
    _can_have_keywords: bool = False
    _do_need_keywords: bool = False
    _can_have_extra_parameters: bool = False

    _config_as_segment: ConfigurationAsSegment = ConfigurationAsSegment(
        type = SegmentType.YOUTUBE_VIDEO,
    )
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.YOUTUBE_VIDEO,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.YOUTUBE_VIDEO,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass

@dataclass
class TextConfiguration(Configuration):
    """
    The 'Text' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.TEXT
    
    _can_have_narration = True
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = True
    _can_have_text: bool = True
    _do_need_text: bool = True
    _can_have_filename: bool = False
    _can_have_url: bool = True
    _do_need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _do_need_keywords: bool = True
    _can_have_extra_parameters: bool = True

    _config_as_segment: ConfigurationAsSegment = ConfigurationAsSegment(
        type = SegmentType.TEXT,
    )
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.TEXT,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.OVERLAY,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.TEXT,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.OVERLAY,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass
    
@dataclass
class MemeConfiguration(Configuration):
    """
    The 'Meme' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.MEME
    
    _can_have_narration = True
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = False
    _can_have_text: bool = False
    _do_need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _do_need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _do_need_keywords: bool = True
    _can_have_extra_parameters: bool = False

    _config_as_segment: ConfigurationAsSegment = ConfigurationAsSegment(
        type = SegmentType.MEME,
        string_durations = [EnhancementStringDuration.FILE_DURATION]
    )
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.MEME,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.INLINE,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION, EnhancementStringDuration.FILE_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.MEME,
        modes = [ShortcodeMode.INLINE, ShortcodeMode.OVERLAY],
        default_mode = ShortcodeMode.INLINE,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT, ShortcodeStringDuration.FILE_DURATION]
    )

    def __init__(
        self
    ):
        pass

@dataclass
class EffectConfiguration(Configuration):
    """
    The 'Effect' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.EFFECT
    
    _can_have_narration = False
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = False
    _do_need_specific_duration: bool = False
    _can_have_text: bool = False
    _do_need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _do_need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _do_need_keywords: bool = True
    _can_have_extra_parameters: bool = True

    _config_as_segment: ConfigurationAsSegment = None
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.EFFECT,
        modes = [EnhancementMode.REPLACE, EnhancementMode.INLINE],
        default_mode = EnhancementMode.REPLACE,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.EFFECT,
        modes = [ShortcodeMode.REPLACE, ShortcodeMode.INLINE],
        default_mode = ShortcodeMode.REPLACE,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass
    
@dataclass
class PremadeConfiguration(Configuration):
    """
    The 'Premade' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.PREMADE
    
    _can_have_narration = True
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = True
    _can_have_text: bool = False  # dynamic parameters will be applied
    _do_need_text: bool = False
    _can_have_filename: bool = False
    _can_have_url: bool = False
    _do_need_filename_or_url: bool = False
    _can_have_keywords: bool = True
    _do_need_keywords: bool = True
    _can_have_extra_parameters: bool = True

    _config_as_segment: ConfigurationAsSegment = ConfigurationAsSegment(
        type = SegmentType.PREMADE,
    )
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.PREMADE,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.INLINE,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.PREMADE,
        modes = [EnhancementMode.INLINE, EnhancementMode.OVERLAY],
        default_mode = EnhancementMode.INLINE,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass
    
@dataclass
class GreenscreenConfiguration(Configuration):
    """
    The 'Greenscreen' element configuration, that defines if it can
    be used as a segment or as a enhancement (or both) and all the
    things it needs to work as expected.
    """
    _type = _Type.GREENSCREEN
    
    _can_have_narration = False
    _do_need_voice_narration: bool = False
    _can_have_specific_duration: bool = True
    _do_need_specific_duration: bool = False
    _can_have_text: bool = False  # dynamic parameters will be applied
    _do_need_text: bool = False
    _can_have_filename: bool = True
    _can_have_url: bool = True
    _do_need_filename_or_url: bool = True
    _can_have_keywords: bool = False
    _do_need_keywords: bool = False
    _can_have_extra_parameters: bool = False

    _config_as_segment: ConfigurationAsSegment = None
    _config_as_enhancement: ConfigurationAsEnhancement = ConfigurationAsEnhancement(
        type = EnhancementType.GREENSCREEN,
        modes = [EnhancementMode.REPLACE],
        default_mode = EnhancementMode.REPLACE,
        string_durations = [EnhancementStringDuration.SEGMENT_DURATION]
    )
    _config_as_shortcode: ConfigurationAsShortcode = ConfigurationAsShortcode(
        type = ShortcodeType.GREENSCREEN,
        modes = [EnhancementMode.REPLACE],
        default_mode = EnhancementMode.REPLACE,
        string_durations = [ShortcodeStringDuration.SHORTCODE_CONTENT]
    )

    def __init__(
        self
    ):
        pass
