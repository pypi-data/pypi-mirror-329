from yta_core.builder import Builder
from yta_core.builder.stock_builder import StockBuilder
from yta_core.enums.field import EnhancementField, SegmentField
from yta_core.builder.youtube import YoutubeDownloader
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.logger import print_in_progress
from moviepy import VideoFileClip, concatenate_videoclips
from typing import Union


class CustomStockBuilder(Builder):
    """
    The builder of the AI_VIDEO type.
    """

    @staticmethod
    def build_from_enhancement(
        enhancement: dict
    ):
        """
        Build the video content from the information
        in the given 'enhancement' dict.
        """
        ParameterValidator.validate_mandatory_dict('enhancement', enhancement)

        return CustomStockBuilder.build(
            enhancement.get(EnhancementField.KEYWORDS.value, None),
            enhancement.get(EnhancementField.DURATION.value, None)
        )

    @staticmethod
    def build_from_segment(
        segment: dict
    ):
        """
        Build the video content from the information
        in the given 'segment' dict.
        """
        ParameterValidator.validate_mandatory_dict('segment', segment)

        return CustomStockBuilder.build(
            segment.get(SegmentField.KEYWORDS.value, None),
            segment.get(SegmentField.DURATION.value, None)
        )
    
    @classmethod
    def build(
        cls,
        keywords: str,
        duration: Union[float, int]
    ):
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        
        youtube_downloader = YoutubeDownloader()

        # TODO: This way of building the final video has
        # to be reviewed
        videos = []
        do_use_youtube = True # to stop searching in Youtube if no videos available
        accumulated_duration = 0
        while accumulated_duration < duration:
            downloaded_video = None
            if do_use_youtube:
                # We try to download if from Youtube
                print_in_progress('Downloading youtube stock video')
                youtube_stock_video = youtube_downloader.get_stock_video(keywords)
                if youtube_stock_video is not None:
                    downloaded_video = youtube_stock_video.download()
                    if downloaded_video is not None:
                        youtube_downloader.ignore_id(youtube_stock_video.id)

            if downloaded_video is None:
                # Not found or not searching on Youtube, so build 'stock'
                print_in_progress('Downloading stock video (youtube not found)')
                do_use_youtube = False
                video = StockBuilder.build(keywords, duration)
            else:
                video = VideoFileClip(downloaded_video.output_filename)

            accumulated_duration += video.duration

            if accumulated_duration > duration:
                end = video.duration - (accumulated_duration - duration)
                start = 0
                if (
                    youtube_stock_video and
                    youtube_stock_video.key_moment != 0 and
                    youtube_stock_video.key_moment is not None
                ):
                    # Ok, lets use that key moment as the center of our video
                    start = youtube_stock_video.key_moment - (end / 2)
                    end = youtube_stock_video.key_moment + (end / 2)
                    if start < 0:
                        end += abs(0 - start)
                        start = 0
                    if end > video.duration:
                        start -= abs(end - video.duration)
                        end = video.duration
                video = video.with_subclip(start, end)

            videos.append(video)

        return concatenate_videoclips(videos)