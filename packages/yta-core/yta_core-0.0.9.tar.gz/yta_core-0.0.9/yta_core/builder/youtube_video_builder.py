from yta_core.builder import Builder
from yta_core.builder.youtube import YoutubeDownloader
from yta_core.enums.field import EnhancementField, SegmentField
from yta_core.settings import Settings
from yta_general_utils.programming.validator.parameter import ParameterValidator
from moviepy import VideoFileClip, concatenate_videoclips
from moviepy.Clip import Clip
from typing import Union


class YoutubeVideoBuilder(Builder):
    """
    The builder of the YOUTUBE_VIDEO type.
    """

    @staticmethod
    def build_from_enhancement(
        enhancement: dict
    ) -> Clip:
        ParameterValidator.validate_mandatory_dict('enhancement', enhancement)

        return YoutubeVideoBuilder.build(
            enhancement.get(EnhancementField.URL.value, None),
            enhancement.get(EnhancementField.DURATION.value, None)
        )

    @staticmethod
    def build_from_segment(
        segment: dict
    ) -> Clip:
        ParameterValidator.validate_mandatory_dict('segment', segment)

        return YoutubeVideoBuilder.build(
            segment.get(SegmentField.URL.value, None),
            segment.get(SegmentField.DURATION.value, None)
        )

    @staticmethod
    def build(
        url: str,
        duration: Union[float, int]
    ) -> Clip:
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)

        # Get the youtube video
        youtube_downloader = YoutubeDownloader()
        # This will raise an Exception if not available
        youtube_video = youtube_downloader.get_video(url)

        # TODO: We should handle different types of build
        # processes when a YOUTUBE_VIDEO is requested with
        # a 'strategy' field or something. What about
        # 'hot_moments', 'random_scenes', 'summarize' (?)
        # TODO: What if asking for an 'strategy' that is 
        # not available (?)
        STRATEGY = 'HOT_MOMENTS'

        number_of_scenes = duration // Settings.MAX_DURATION_PER_YOUTUBE_SCENE
        if (duration + Settings.MAX_DURATION_PER_YOUTUBE_SCENE) > 0:
            number_of_scenes += 1

        duration_of_scene = duration / number_of_scenes

        # TODO: Build 'number_of_scene' scenes of 'duration_of_scene'
        # seconds of duration according to the strategy
        
        # TODO: Validate if it is possible to build
        if (
            STRATEGY == 'HOT_MOMENTS' and
            not youtube_video.has_most_viewed_scenes
        ):
            raise Exception(f'The youtube video {youtube_video.id} does not have most viewed scenes.')

        if STRATEGY == 'HOT_MOMENTS':
            scenes = youtube_video.most_viewed_scenes

        # TODO: We need to build the scenes with 'duration_of_scene'
        # and 'number_of_scenes'

        # youtube_video_scenes = []
        # if youtube_video.heatmap:
        #     youtube_video_scenes = youtube_video.get_hottest_scenes(scenes_number, scene_duration)
        # else:
        #     youtube_video_scenes = youtube_video.get_scenes(scenes_number, scene_duration)

        # Now we have all scenes, subclip the youtube clip
        youtube_clip = VideoFileClip(youtube_downloader.download_this_video(youtube_video))

        # TODO: By now, as I don't have strategies to apply, I
        # am just subclipping the video in the middle
        return youtube_clip.with_subclip(youtube_video.duration - (duration / 2), youtube_video.duration + (duration / 2))

        return concatenate_videoclips([
            youtube_clip.with_subclip(scene.start_time, scene.end_time)
            for scene in scenes
        ])