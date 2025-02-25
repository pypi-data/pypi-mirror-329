from yta_core.builder.youtube.enums import YoutubeChannelId
from yta_youtube.api import YoutubeAPI
from yta_youtube.enums import VideoFormatQuality, YoutubeVideoLanguage, AudioFormatQuality
from yta_youtube_enhanced.video import YoutubeVideo
from yta_general_utils.programming.decorators import singleton
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.random import Random
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from typing import Union

import requests


__all__ = [
    'YoutubeDownloader'
]

@singleton
class YoutubeDownloader:
    """
    Singleton class.

    This object simplifies the access to our Youtube
    provider channels. It uses the Google Youtube Data
    V3 API and, if not available, uses a community API
    to obtain the videos.

    This object is used to download memes, stock videos,
    sounds, music, etc. from our specific Youtube channels.
    """

    _ids_to_ignore: list[str]
    """
    The ids that have been previously downloaded and 
    have to be ignored in the next searches.
    """
    _do_ignore_ids: bool
    """
    A flag to indicate if previously downloaded ids 
    (that are stored in the internal '_ids_to_ignore'
    attribute) have to be ignored or not.
    """
    _service: any
    """
    Youtube service to search though the using keywords.
    """
    
    def __init__(
        self,
        do_ignore_ids: bool = True
    ):
        if not YoutubeAPI.is_youtube_token_valid():
            print('Youtube token is not valid. Please, login to get a new valid token.')
            YoutubeAPI.start_youtube_auth_flow()

        self._service = YoutubeAPI.create_youtube_service()
        self._do_ignore_ids = do_ignore_ids
        self._ids_to_ignore = []
        
    def activate_ignore_repeated(
        self
    ) -> None:
        """
        Set as True the internal flag that indicates 
        that the ids of the videos that are downloaded
        after being activated have to be ignored in 
        the next downloads, so each video is downloaded
        only once.
        """
        self._do_ignore_ids = True

    def deactivate_ignore_repeated(
        self
    ) -> None:
        """
        Set as False the internal flag that indicates 
        that the ids of the videos that are downloaded
        after being activated have to be ignored in 
        the next downloads, so each video can be 
        downloaded an unlimited amount of times.
        """
        self._do_ignore_ids = True

    def ignore_id(
        self,
        id_to_ignore: str
    ) -> None:
        """
        Add the provided 'id_to_ignore' id to the list of
        ids to ignore.
        """
        if id_to_ignore not in self._ids_to_ignore:
            self._ids_to_ignore.append(id_to_ignore)

    def reset(
        self
    ) -> None:
        """
        Empty the internal list of ids to ignore.
        """
        self._ids_to_ignore = []

    def get_video(
        self,
        id_or_url: str
    ) -> YoutubeVideo:
        """
        Returns a YoutubeVideo instance with the video
        that has the given 'id_or_url' id or url.
        """
        ParameterValidator.validate_mandatory_string('id_or_url', id_or_url, do_accept_empty = False)
        
        return YoutubeVideo(id_or_url)
    
    def download_this_video(
        self,
        youtube_video: YoutubeVideo,
        do_include_audio: bool = True,
        language: YoutubeVideoLanguage = YoutubeVideoLanguage.DEFAULT,
        output_filename: Union[str, None] = None
    ) -> Union[str, None]:
        """
        Download the provided 'youtube_video' with a maximum
        of FULL_HD (1920x1080) and store it locally. The 
        video will be downloaded with audio if the
        'do_include_audio' flag is True, and will be 
        downloaded in the given 'language' if available.

        TODO: Careful, 'language' could be not available, by
        now we are returning None in that situation.
        """
        ParameterValidator.validate_mandatory_instance_of('youtube_video', youtube_video, YoutubeVideo)
        language = YoutubeVideoLanguage.to_enum(language)
        output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)

        if (
            do_include_audio and
            not youtube_video.is_audio_language_available(language)
        ):
            return None
    
        downloaded_video = (
            youtube_video.download_with_best_quality(
                language = language,
                video_quality = VideoFormatQuality.FULL_HD,
                output_filename = output_filename
            )
            if do_include_audio else
            youtube_video.download_video_with_best_quality(
                video_quality = VideoFormatQuality.FULL_HD,
                output_filename = output_filename
            )
        )

        self.ignore_id(downloaded_video.id)

        return downloaded_video.output_filename

    def download_video(
        self,
        url: str,
        do_include_audio: bool = True,
        language: YoutubeVideoLanguage = YoutubeVideoLanguage.DEFAULT,
        output_filename: Union[str, None] = None
    ) -> Union[str, None]:
        """
        Download the video from the given 'url', including
        or not the sound depending on the 'do_include_audio'
        parameter, using the provided 'language' (that could
        be not available), and storing it locally as
        'output_filename'.

        This method will return the local filename in which
        the video has been downloaded, or None if it was not
        possible to download it.
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        ParameterValidator.validate_mandatory_bool('do_include_audio', do_include_audio)
        language = YoutubeVideoLanguage.to_enum(language)

        try:
            # TODO: This will raise an Exception if not available
            youtube_video = YoutubeVideo(url)
        except: 
            return None
        
        return self.download_this_video(
            youtube_video,
            do_include_audio = do_include_audio,
            language = language,
            output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)
        )
    
    def download_audio(
        self,
        url: str,
        language: YoutubeVideoLanguage = YoutubeVideoLanguage.DEFAULT,
        output_filename: str = None
    ):
        """
        Download the video audio from the given 'url', using
        the provided 'language' (that could be not available),
        and storing it locally as 'output_filename'.

        This method will return the local filename in which
        the audio has been downloaded, or None if it was not
        possible to download it.
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        language = YoutubeVideoLanguage.to_enum(language)
        video = YoutubeVideo(url)

        downloaded_audio = video.download_audio(
            language = language,
            output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        )

        self.ignore_id(downloaded_audio.id)

        return downloaded_audio.output_filename

    # TODO: Append all the 'download_x' (from channel) here below
    def download_meme_video(
        self,
        keywords: str,
        do_include_audio: bool = True,
        do_randomize: bool = False,
        output_filename: Union[str, None] = None
    ) -> Union[str, None]:
        """
        Download a meme from the specific Meme youtube channel
        including the audio if the 'do_include_audio' parameter
        is True. It will choose a random video if the
        'do_randomize' parameter is set as True, or the first
        one found if False.

        This method returns the 'output_filename' with which 
        the video has been downloaded locally, or None if no
        one was found.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        ParameterValidator.validate_mandatory_bool('do_include_audio', do_include_audio)
        ParameterValidator.validate_mandatory_bool('do_randomize', do_randomize)

        return self._download_video(
            keywords = keywords,
            channel_id = YoutubeChannelId.MEMES,
            do_include_audio = do_include_audio,
            do_randomize = do_randomize,
            output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)
        )
    
    def download_stock_video(
        self,
        keywords: str,
        do_include_audio: bool = True,
        do_randomize: bool = False,
        output_filename: Union[str, None] = None
    ) -> Union[str, None]:
        """
        Download a stock video from the specific Stock youtube
        channel including the audio if the 'do_include_audio'
        parameter is True. It will choose a random video if the
        'do_randomize' parameter is set as True, or the first
        one found if False.

        This method returns the 'output_filename' with which 
        the video has been downloaded locally, or None if no
        one was found.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        ParameterValidator.validate_mandatory_bool('do_include_audio', do_include_audio)
        ParameterValidator.validate_mandatory_bool('do_randomize', do_randomize)
        
        return self._download_video(
            keywords = keywords,
            channel_id = YoutubeChannelId.STOCK,
            do_include_audio = do_include_audio,
            do_randomize = do_randomize,
            output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)
        )
    
    def download_sound_audio(
        self,
        keywords: str,
        output_filename: Union[str, None] = None
    ) -> Union[str, None]:
        """
        Download a sound audio from the specific Sounds youtube
        channel.

        This method returns the 'output_filename' with which 
        the audio has been downloaded locally, or None if no
        one was found.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)

        return self._download_audio(
            keywords = keywords,
            channel_id = YoutubeChannelId.SOUNDS,
            do_randomize = False,
            output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        )

    def download_music_audio(
        self,
        keywords: str,
        output_filename: Union[str, None] = None
    ) -> Union[str, None]:
        """
        Download a music audio from the specific Music youtube
        channel.

        This method returns the 'output_filename' with which 
        the audio has been downloaded locally, or None if no
        one was found.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)

        return self._download_audio(
            keywords = keywords,
            channel_id = YoutubeChannelId.MUSIC,
            do_randomize = False,
            output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        )
    
    def get_stock_video(
        self,
        keywords: str,
        do_randomize: bool = False
    ) -> Union[YoutubeVideo, None]:
        """
        Get a stock video from the Stock youtube video
        channel that matches the provided 'keywords'. It
        will return the first one or a random one if the
        'do_randomize' parameter is set as True.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        
        return self._get_video_from_keywords(keywords, YoutubeChannelId.STOCK, do_randomize)
    
    # TODO: Append all the 'download_x' (from channel) here above

    def _get_video_from_keywords(
        self,
        keywords: str,
        channel_id: YoutubeChannelId,
        do_randomize: bool = False
    ) -> Union[YoutubeVideo, None]:
        """
        Look for a video in the channel with the given
        'channel_id' id that is obtained with the also
        provided 'keywords'. The result will be the first
        one found or a random one if 'do_randomize' is 
        True.

        This method will ignore the previously downloaded
        videos only if that internal flag is activated.
        You can activate it by using the 
        'activate_ignore_ids' method.

        For internal use only.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        channel_id = YoutubeChannelId.to_enum(channel_id)
        ParameterValidator.validate_mandatory_bool('do_randomize', do_randomize)

        youtube_videos = self._search(keywords, 25, channel_id)

        if len(youtube_videos) == 0:
            return None
        
        # Remove the previously downloaded videos
        if (
            self._do_ignore_ids and
            len(self._ids_to_ignore) > 0
        ):
            youtube_videos = [
                youtube_video
                for youtube_video in youtube_videos
                if youtube_video['id']['videoId'] not in self._ids_to_ignore
            ]

        if len(youtube_videos) == 0:
            return None
        
        return YoutubeVideo(
            youtube_videos[0]
            if not do_randomize else
            youtube_videos[Random.int_between(0, len(youtube_videos) - 1)]
        )

    def _search(
        self,
        keywords: str,
        max_results: int = 25,
        channel_id: YoutubeChannelId = None
    ) -> list[any]:
        """
        Look for videos in the channel with the given
        'channel_id' id that are obtained with the also
        provided 'keywords'. The number of results will
        be, as maximum, the given 'max_results' parameter.

        This method returns all the videos that have been
        found with those parameters.

        For internal use only.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        channel_id = YoutubeChannelId.to_enum(channel_id)
        max_results = 25 if max_results is None else max_results

        try:
            response_videos_list = self._service.search().list(
                part = 'snippet',
                channelId = channel_id.value,
                maxResults = max_results,
                order = 'relevance',  # This is the most interesting by far, using the youtube search engine
                type = 'video',
                q = keywords
            ).execute()
        except Exception as e:
            print(e)
            # We try the collaborative known alternative that should work
            no_key_url = f'https://yt.lemnoslife.com/noKey/search?part=snippet&channelId={channel_id.value}&maxResults={str(max_results)}&order=relevance&type=video&q={keywords}&alt=json'

            try:
                response_videos_list = requests.get(no_key_url).json()
            except Exception as e:
                print(e)
                return []

        return (
            response_videos_list['items']
            if response_videos_list['pageInfo']['totalResults'] > 0 else
            []
        )
    
    def _download_video(
        self,
        keywords: str,
        channel_id: YoutubeChannelId,
        do_include_audio: bool = False,
        do_randomize: bool = False,
        output_filename: Union[str, None] = None
    ) -> Union[None, str]:
        """
        Look for a video in the channel with the given
        'channel_id' id that is obtained with the also
        provided 'keywords'. The result will be the first
        one found or a random one if 'do_randomize' is 
        True.

        This method will ignore the previously downloaded
        videos only if that internal flag is activated.
        You can activate it by using the 
        'activate_ignore_ids' method.

        This method will return None if no videos found or
        the download was not possible, or the filename
        with which the video has been downloaded if it was
        possible.

        This method forces the download to FULL HD quality
        (1920x1080) or lower if unavailable.

        For internal use only.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        channel_id = YoutubeChannelId.to_enum(channel_id)
        ParameterValidator.validate_mandatory_bool('do_include_audio', do_include_audio)
        ParameterValidator.validate_mandatory_bool('do_randomize', do_randomize)
        
        youtube_video = self._get_video_from_keywords(keywords, channel_id, do_randomize)

        if not youtube_video:
            return None

        download_method = (
            lambda video_quality, output_filename: youtube_video.download_with_best_quality(
                video_quality = video_quality,
                output_filename = output_filename
            )
            if do_include_audio else
            lambda video_quality, output_filename: youtube_video.download_video_with_best_quality(
                video_quality = video_quality,
                output_filename = output_filename
            )
        )

        output_filename = download_method(
            VideoFormatQuality.FULL_HD,
            Output.get_filename(output_filename, FileTypeX.VIDEO)
        )

        if self._do_ignore_ids:
            self.ignore_id(youtube_video.id)

        return output_filename
    
    def _download_audio(
        self,
        keywords: str,
        channel_id: YoutubeChannelId,
        do_randomize: bool = False,
        language: YoutubeVideoLanguage = YoutubeVideoLanguage.DEFAULT,
        output_filename: Union[str, None] = None
    ) -> Union[None, str]:
        """
        Look for the audio of a video in the channel with
        the given 'channel_id' id that is obtained with
        the also provided 'keywords'. The result will be
        the first one found or a random one if 'do_randomize'
        is True.

        This method will ignore the previously downloaded
        videos only if that internal flag is activated.
        You can activate it by using the 
        'activate_ignore_ids' method.

        This method will return None if no videos found or
        the download was not possible, or the filename
        with which the video has been downloaded if it was
        possible.

        This method will download the best audio quality
        available.

        For internal use only.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        channel_id = YoutubeChannelId.to_enum(channel_id)
        ParameterValidator.validate_mandatory_bool('do_randomize', do_randomize)
        
        youtube_video = self._get_video_from_keywords(keywords, channel_id, do_randomize)

        if not youtube_video:
            return None
        
        youtube_video.download_audio_with_best_quality(
            language = language,
            quality = AudioFormatQuality.BEST,
            output_filename = Output.get_filename(output_filename, FileTypeX.AUDIO)
        )

        if self._do_ignore_ids:
            self.ignore_id(youtube_video.id)

        return output_filename