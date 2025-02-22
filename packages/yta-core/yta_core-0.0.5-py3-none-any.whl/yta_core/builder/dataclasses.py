from yta_multimedia.video.utils import generate_video_from_image
from yta_image.generation.ai.generator import DefaultImageGenerator
from dataclasses import dataclass
from typing import Union


@dataclass
class ClippableImage:
    """
    @dataclass
    Class to wrap the information about an Image that
    can be turned into a video clip.
    """

    duration: float
    """
    The expected duration of the AI Image when converted
    to a video clip.
    """
    _video_effect: Union[any, None]
    """
    The effect that will be applied when generating
    the video clip of the given 'duration'.

    TODO: This must be implemented in a near future
    """
    _filename: str
    """
    The filename of the image.
    """

    @property
    def image(
        self
    ) -> str:
        """
        The image filename.

        TODO: This could be a pillow Image instance.
        """
        return self._filename
    
    @property
    def video(
        self
    ) -> str:
        """
        The video generated with the also generated
        image and lasting the provided 'duration'.
        """
        if not self.image:
            return None
            
        if not hasattr(self, '_video_filename'):
            self._video_filename = generate_video_from_image(
                self.image,
                self.duration,
                fps = 60,
                # TODO: Implement the effect
                #self._video_effect
            )

        # TODO: Return it parsed as VideoFileClip (?)
        return self._video_filename
    
    def __init__(
        self,
        filename: str,
        duration: float,
        # TODO: Make this 'video_effect' more strict
        video_effect: Union[any, None] = None
    ) -> 'ClippableImage':
        # TODO: Validate it is a valid image filename (?)
        self._filename = filename
        self.duration = duration
        self._video_effect = video_effect

@dataclass
class AIImage(ClippableImage):
    """
    Class to wrap the information about an AI Image
    that is used within the AIImageBuilder.
    """

    _prompt: str
    """
    The prompt that will be used to generate the
    image.
    """
    duration: float
    """
    The expected duration of the AI Image as a clip.
    """
    _video_effect: Union[any, None]
    """
    The effect that will be applied when generating
    the video clip of the given 'duration'.
    """

    @property
    def image(
        self
    ) -> str:
        """
        The AI Image generated with the given 'prompt'.
        This method will generate the image the first
        time it is called.
        """
        if not hasattr(self, '_filename'):
            self._filename = DefaultImageGenerator().generate_image(self._prompt).filename

        # TODO: Return it parsed as Image (?)
        return self._filename
    
    def __init__(
        self,
        prompt: str,
        duration: float,
        # TODO: Make this 'video_effect' more strict
        video_effect: Union[any, None] = None
    ) -> 'AIImage':
        self._prompt = prompt
        self.duration = duration
        self._video_effect = video_effect
        self.filename = None
    
    def reset(
        self
    ):
        """
        Reset the instance to forget any previously
        generated image or video, so it will be 
        generated again the next time 'image' or
        'video' property is accessed.
        """
        self._filename = None
        self._video_filename = None
