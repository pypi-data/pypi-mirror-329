from yta_core.builder import Builder
from yta_core.builder.dataclasses import ClippableImage
from yta_core.builder.stock import StockDownloader
from yta_core.builder.ai_image_builder import AIImageBuilder
from yta_core.enums.field import EnhancementField, SegmentField
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_multimedia.video.edition.resize import resize_video, ResizeMode
from yta_general_utils.logger import print_in_progress
from moviepy import concatenate_videoclips, VideoFileClip
from typing import Union


class StockBuilder(Builder):
    """
    The builder of the STOCK type.
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

        return StockBuilder.build(
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

        return StockBuilder.build(
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
        
        stock_downloader = StockDownloader(do_ignore_repeated = True)
        
        videos = []
        accumulated_duration = 0
        while accumulated_duration < duration:
            print_in_progress('Downloading stock video')
            # TODO: Make this force 1920x1080 resolution
            downloaded_filename = stock_downloader.download_video(
                keywords = keywords,
                # Maybe randomizing is not good because the
                # best results are the first ones
                do_randomize = True
            )

            # If no video, download stock image
            if not downloaded_filename:
                downloaded_filename = stock_downloader.download_image(
                    keywords = keywords,
                    # Maybe randomizing is not good because the
                    # best results are the first ones
                    do_randomize = True
                )

                if downloaded_filename:
                    video = VideoFileClip(ClippableImage(downloaded_filename, duration - accumulated_duration).video)
                else:
                    # No stock videos available, lets build with AI images
                    # TODO: Maybe we should improve the prompt for stock AI
                    # images and set it as a common method
                    video = AIImageBuilder.build(keywords, duration - accumulated_duration)
                    # TODO: If 'video' fails here... omg..., but can happen
            else:
                video = VideoFileClip(downloaded_filename)

            # Resize the video to fit custom scene size
            # TODO: Read these values from size constants
            video = resize_video(video, (1920, 1080), resize_mode = ResizeMode.RESIZE_KEEPING_ASPECT_RATIO)

            accumulated_duration += video.duration
            # Last clip must be cropped to fit the expected duration
            if accumulated_duration > duration:
                video = video.with_subclip(0, video.duration - (accumulated_duration - duration))
            # TODO: I'm forcing 1920, 1080 here but it must come from Pexels
            videos.append(video)

        return concatenate_videoclips(videos)