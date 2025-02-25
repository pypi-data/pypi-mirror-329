from yta_stock_downloader import StockVideoDownloader, StockImageDownloader
from yta_general_utils.programming.decorators import singleton
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from typing import Union


__all__ = [
    'StockDownloader'
]

@singleton
class StockDownloader:
    """
    Singleton class.

    This object simplifies the access to stock videos
    from official platforms. It uses the different
    platforms APIs.
    """

    _do_ignore_ids: bool
    """
    A flag to indicate if previously downloaded ids 
    (that are stored in the internal attributes to
    ignore from each platform) have to be ignored or
    not.
    """

    @property
    def do_ignore_ids(
        self
    ) -> bool:
        return self._do_ignore_ids
    
    @do_ignore_ids.setter
    def do_ignore_ids(
        self,
        value: bool
    ) -> None:
        self._do_ignore_ids = value
        self._video_downloader._do_ignore_ids = value
        self._image_downloader._do_ignore_ids = value

    def __init__(
        self,
        do_ignore_ids: bool = True
    ):
        self._video_downloader = StockVideoDownloader(do_ignore_ids = do_ignore_ids)
        self._image_downloader = StockImageDownloader(do_ignore_ids = do_ignore_ids)
        self._do_ignore_ids = do_ignore_ids

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
        self.do_ignore_ids = True

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
        self.do_ignore_ids = True

    def reset(
        self
    ):
        """
        This method will empty the array that handles 
        the duplicated ids (if activated) to enable 
        downloading any resource found again. This
        method will also reset its platform-specific 
        downloader instances.
        """
        self._video_downloader.reset()
        self._image_downloader.reset()

    def download_video(
        self,
        keywords: str,
        do_randomize: bool = False,
        output_filename: Union[str, None] = None
    ) -> Union[str, None]:
        """
        Download a video with the given 'keywords' from the
        stock platforms. The video will be the first found
        or a random one if 'do_randomize' is True.

        This method will return the filename of the video
        once it's been downloaded and stored locally, or
        None if no one was found.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        ParameterValidator.validate_mandatory_bool('do_randomize', do_randomize)
        
        download_method = (
            lambda query, output_filename: self._video_downloader.download_random(
                query = query,
                output_filename = output_filename
            )
            if do_randomize else
            lambda query, output_filename: self._video_downloader.download(
                query = query,
                output_filename = output_filename
            )
        )

        # TODO: What about the sound (?)
        try:
            video = download_method(
                query = keywords,
                output_filename = Output.get_filename(output_filename, FileTypeX.VIDEO)
            )
        except:
            pass

        # TODO: Should we try the 'download_image' if no video
        # available? Or should that strategy be built in the
        # part that requests it (?)

        # TODO: Should I return the FileReturn instead (?)
        return (
            video.filename
            if video is not None else
            None
        )
    
    def download_image(
        self,
        keywords: str,
        do_randomize: bool = False,
        output_filename: Union[str, None] = None
    ) -> Union[str, None]:
        """
        Download an image with the given 'keywords' from the
        stock platforms. The image will be the first found
        or a random one if 'do_randomize' is True.

        This method will return the filename of the image
        once it's been downloaded and stored locally, or
        None if no one was found.
        """
        ParameterValidator.validate_mandatory_string('keywords', keywords, do_accept_empty = False)
        ParameterValidator.validate_mandatory_bool('do_randomize', do_randomize)

        download_method = (
            lambda query, output_filename: self._image_downloader.download_random(
                query = query,
                output_filename = output_filename
            )
            if do_randomize else
            lambda query, output_filename: self._image_downloader.download(
                query = query,
                output_filename = output_filename
            )
        )

        try:
            image = download_method(
                query = keywords,
                output_filename = Output.get_filename(output_filename, FileTypeX.IMAGE)
            )
        except:
            pass

        # TODO: Should I return the FileReturn instead (?)
        return (
            image.filename
            if image is not None else
            None
        )