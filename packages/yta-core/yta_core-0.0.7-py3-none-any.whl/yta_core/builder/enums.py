from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_multimedia.video.edition.effect.black_and_white_effect import BlackAndWhiteEffect
from yta_multimedia.video.edition.effect.blink_effect import BlinkEffect
from yta_multimedia.video.edition.effect.blur_effect import BlurEffect
from yta_multimedia.video.edition.effect.fade_in_effect import FadeInEffect
from yta_multimedia.video.edition.effect.fade_out_effect import FadeOutEffect
from yta_multimedia.video.edition.effect.flip_vertically_effect import FlipVerticallyEffect
from yta_multimedia.video.edition.effect.flip_horizontally_effect import FlipHorizontallyEffect
from yta_multimedia.video.edition.effect.multiplied_effect import MultipliedEffect
from yta_multimedia.video.edition.effect.photo_is_taken_effect import PhotoIsTakenEffect
from yta_multimedia.video.edition.effect.reversed_effect import ReversedEffect
from yta_multimedia.video.edition.effect.sad_moment_effect import SadMomentEffect
from yta_multimedia.video.edition.effect.scroll_effect import ScrollEffect
from yta_multimedia.video.edition.effect.zoom.zoom_video_effect import ZoomVideoEffect
from yta_multimedia.video.edition.effect.stop_motion_effect import StopMotionEffect
from yta_multimedia.video.edition.effect.artisanal.dynamic_postcard_effect import DynamicPostcardEffect
from yta_multimedia.video.edition.effect.artisanal.zoom_in_display_and_zoom_out_effect import ZoomInDisplayAndZoomOutEffect
from yta_multimedia.video.generation.manim.classes.text.test_text_manim_animation import TestTextManimAnimationWrapper as TestTextManimAnimation
from yta_multimedia.video.generation.manim.classes.text.magazine_text_is_written_manim_animation import MagazineTextIsWrittenManimAnimationWrapper as MagazineTextIsWrittenManimAnimation
from yta_multimedia.video.generation.manim.classes.text.magazine_text_static_manim_animation import MagazineTextStaticManimAnimationWrapper as MagazineTextStaticManimAnimation
from yta_multimedia.video.generation.manim.classes.text.rain_of_words_manim_animation import RainOfWordsManimAnimationWrapper as RainOfWordsManimAnimation
from yta_multimedia.video.generation.manim.classes.text.simple_text_manim_animation import SimpleTextManimAnimationWrapper as SimpleTextManimAnimation
from yta_multimedia.video.generation.manim.classes.text.text_word_by_word_manim_animation import TextWordByWordManimAnimationWrapper as TextWordByWordManimAnimation
from yta_multimedia.video.generation.manim.classes.text.text_triplets_manim_animation import TextTripletsManimAnimationWrapper as TextTripletsManimAnimation
from yta_multimedia.video.generation.google.google_search import GoogleSearch
from yta_multimedia.video.generation.google.youtube_search import YoutubeSearch
# from yta_multimedia.video.generation.manim.classes.video.test_video_manim_animation import TestVideoMobjectIn2DManimAnimationWrapper as TestVideoMobjectIn2DManimAnimation, TestVideoOpenGLMobjectIn2DManimAnimationWrapper as TestVideoOpenGLMobjectIn2DManimAnimation, TestVideoMobjectIn3DManimAnimationWrapper as TestVideoMobjectIn3DManimAnimation, TestVideoOpenGLMobjectIn3DManimAnimationWrapper as TestVideoOpenGLMobjectIn3DManimAnimation, TestImageOpenGLMobjectIn3DManimAnimationWrapper as TestImageOpenGLMobjectIn3DManimAnimation


class EffectPremade(Enum):
    """
    Effect premade enum class to make our effects available
    by matching the corresponding class. If the Enum exist,
    the effect is applicable.

    TODO: What about this text below: 

    These enums are pretended to be matched by their name ignoring cases,
    so feel free to use the 'get_valid_name' YTAEnum method to obtain the
    valid name to be able to intantiate it.
    """

    # TODO: This has changed completely due to moviepy 2.0.0
    # release, so I need to refactor and rethink about. Here
    # we register the accepted effects, so I think it should
    # be kept, but as I said, lets review it
    BLACK_AND_WHITE = BlackAndWhiteEffect
    BLINK = BlinkEffect
    BLUR = BlurEffect
    FADE_IN = FadeInEffect
    FADE_OUT = FadeOutEffect
    FLIP_HORIZONTALLY = FlipHorizontallyEffect
    FLIP_VERTICALLY = FlipVerticallyEffect
    MULTIPLIED = MultipliedEffect
    PHOTO_IS_TAKEN = PhotoIsTakenEffect
    REVERSED = ReversedEffect
    SAD_MOMENT = SadMomentEffect
    SCROLL = ScrollEffect
    ZOOM = ZoomVideoEffect
    STOP_MOTION = StopMotionEffect
    DYNAMIC_POSTCARD = DynamicPostcardEffect
    ZOOM_IN_OUT = ZoomInDisplayAndZoomOutEffect

class TextPremade(Enum):
    """
    Text premade enum class to make our text videos available
    by matching the corresponding class. If the Enum exist,
    the effect is applicable.

    TODO: What about this text below: 

    These enums are pretended to be matched by their name ignoring cases,
    so feel free to use the 'get_valid_name' YTAEnum method to obtain the
    valid name to be able to intantiate it.
    """
    
    TRIPLETS = TextTripletsManimAnimation
    WORD_BY_WORD = TextWordByWordManimAnimation
    SIMPLE = SimpleTextManimAnimation
    RAIN_OF_WORDS = RainOfWordsManimAnimation
    MAGAZINE_STATIC = MagazineTextStaticManimAnimation
    MAGAZINE_IS_WRITTEN = MagazineTextIsWrittenManimAnimation

    TEST = TestTextManimAnimation

class Premade(Enum):
    """
    Premade enum class to make our premade videos available
    by matching the corresponding class. If the Enum exist,
    the effect is applicable.

    TODO: What about this text below: 

    These enums are pretended to be matched by their name ignoring cases,
    so feel free to use the 'get_valid_name' YTAEnum method to obtain the
    valid name to be able to intantiate it.
    """

    GOOGLE_SEARCH = GoogleSearch
    YOUTUBE_SEARCH = YoutubeSearch
    # These below are just for testing
    # TEST_2D = TestVideoMobjectIn2DManimAnimation
    # TEST_2D_OPENGL = TestVideoOpenGLMobjectIn2DManimAnimation
    # TEST_3D = TestVideoMobjectIn3DManimAnimation
    # TEST_3D_OPENGL = TestVideoOpenGLMobjectIn3DManimAnimation
    # TEST_IMAGE_3D_OPENGL = TestImageOpenGLMobjectIn3DManimAnimation