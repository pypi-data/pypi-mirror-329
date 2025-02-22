from yta_core.classes.segment_json import SegmentJson
from yta_core.enums.field import SegmentBuildingField
from yta_core.enums.status import SegmentStatus
from yta_core.settings import Settings
from yta_core.database import DatabaseHandler
from yta_core.audio.transcription import AudioTranscription
from yta_general_utils.temp import Temp
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.file.handler import FileHandler
from yta_general_utils.logger import print_completed
from yta_general_utils.file.filename import get_file_extension
from moviepy import VideoFileClip, AudioFileClip
from bson.objectid import ObjectId
from typing import Union


class Segment:
    """
    A segment within a Project that is able to build
    itself according to its configuration and values.
    """

    project_id: ObjectId
    """
    The project this segment belongs to.
    """
    index: int
    """
    The index of the segment, which identifies its
    order within the project.
    """
    status: str
    """
    The current status of the segment.
    """
    data: SegmentJson
    """
    The data that the segment has.
    """
    audio_filename: str
    """
    The filename of the audio file.
    """
    video_filename: str
    """
    The filename of the video file.
    """
    full_filename: str
    """
    The filename of the full file that includes
    audio and video.
    """

    @property
    def audio_clip(
        self
    ) -> Union[AudioFileClip, None]:
        """
        The audio clip, from the audio filename if
        existing.
        """
        return (
            AudioFileClip(self.audio_filename)
            if self.audio_filename is not None else
            None
        )

    @property
    def has_audio_clip(
        self
    ) -> bool:
        """
        Check if the segment has an audio clip or not.
        """
        return self.audio_clip is not None
    
    @property
    def video_clip(
        self
    ) -> Union[VideoFileClip, None]:
        """
        The video clip, from the video filename if
        existing.
        """
        return (
            VideoFileClip(self.video_filename)
            if self.video_filename is not None else
            None
        )
    
    @property
    def has_video_clip(
        self
    ) -> bool:
        """
        Check if the segment has a video clip or not.
        """
        return self.video_clip is not None
    
    @property
    def full_clip(
        self
    ) -> Union[VideoFileClip, None]:
        """
        The full clip, including video and audio, from
        the full filename if existing.
        """
        return (
            VideoFileClip(self.full_filename)
            if self.full_filename is not None else
            None
        )
    
    @property
    def has_full_clip(
        self
    ) -> bool:
        """
        Check if the segment has a full clip or not.
        """
        return self.full_clip is not None

    def __init__(
        self,
        project_id: ObjectId,
        index: int,
        data: dict
    ):
        ParameterValidator.validate_mandatory_instance_of('project_id', project_id, ObjectId)
        ParameterValidator.validate_mandatory_int('index', index)

        self.project_id = project_id
        self.index = index

        data = SegmentJson()

        for key in data:
            setattr(data, key, data[key])

        # TODO: Use 'set_audio_filename' (...) here (?)
        self.audio_filename = data.get(SegmentBuildingField.AUDIO_FILENAME.value, None)
        self.video_filename = data.get(SegmentBuildingField.VIDEO_FILENAME.value, None)
        self.full_filename = data.get(SegmentBuildingField.FULL_FILENAME.value, None)

    def build(
        self
    ):
        print_completed('Build completed')
        # TODO: Do it
        pass

    def _set_audio_filename(
        self,
        audio_filename: Union[str, None]
    ):
        """
        Set the 'audio_filename' parameter and update
        it in the database.
        """
        ParameterValidator.validate_string('audio_filename', audio_filename, do_accept_empty = False)

        self.audio_filename = audio_filename

        if audio_filename is not None:
            DatabaseHandler().update_project_segment_field(
                self.project_id,
                self.index,
                SegmentBuildingField.AUDIO_FILENAME.value,
                self.audio_filename
            )

    def _set_video_filename(
        self,
        video_filename: Union[str, None]
    ):
        """
        Set the 'video_filename' parameter and update
        it in the database.
        """
        ParameterValidator.validate_string('video_filename', video_filename, do_accept_empty = False)

        self.video_filename = video_filename

        if video_filename is not None:
            DatabaseHandler().update_project_segment_field(
                self.project_id,
                self.index,
                SegmentBuildingField.VIDEO_FILENAME.value,
                self.video_filename
            )

    def _set_full_filename(
        self,
        full_filename: Union[str, None]
    ):
        """
        Set the 'video_filename' parameter and update
        it in the database.
        """
        ParameterValidator.validate_string('full_filename', full_filename, do_accept_empty = False)

        self.full_filename = full_filename

        if full_filename is not None:
            DatabaseHandler().update_project_segment_field(
                self.project_id,
                self.index,
                SegmentBuildingField.FULL_FILENAME.value,
                self.full_filename
            )

    def _set_transcription(
        self,
        transcription: AudioTranscription
    ):
        """
        Set the transcription in the instance and also in
        the database.
        """
        ParameterValidator.validate_instance_of('transcription', transcription)

        self.transcription = transcription

        if transcription is not None:
            DatabaseHandler().update_project_segment_field(
                self.project_id,
                self.index,
                SegmentBuildingField.TRANSCRIPTION.value,
                self.transcription.for_mongo
            )

    def set_shortcodes(
        self,
        shortcodes
    ):
        #  TODO: What type are these ones (?)
        self.shortcodes = shortcodes

        if shortcodes is not None:
            DatabaseHandler().update_project_segment_field(
                self.project_id,
                self.index,
                SegmentBuildingField.SHORTCODES.value,
                self.shortcodes
            )

    def set_as_finished(
        self
    ):
        """
        Set the segment as finished (building has been
        completed).
        """
        DatabaseHandler().update_project_segment_status(
            self.project_id,
            self.index,
            SegmentStatus.FINISHED.value,
        )

    def _create_segment_file(
        self,
        filename: str
    ):
        """
        Create a filename within the definitive segments
        folder to keep the generated file locally and
        recover it later if something goes wrong.

        The definitive filename will be built using the 
        provided 'filename' and adding some more
        information in the name like the current segment
        index.
        """
        ParameterValidator.validate_mandatory_string('filename', filename, do_accept_empty = False)

        return f'{Settings.DEFAULT_SEGMENT_PARTS_FOLDER}/segment_{self.index}_{Temp.get_filename(filename)}'
    
    def _create_narration(self):
        """
        Creates the audio narration (if needed) by generating an AI audio
        narration with provided 'voice' and 'text_to_narrate'
        parameters or by using the 'audio_narration_filename'.

        This method will set the 'audio_filename' to be able to build the
        audio clip in a near future.
        """
        if self.audio_narration_filename:
            segment_part_filename = self._create_segment_file(f'narration.{get_file_extension(self.audio_narration_filename)}')
            FileHandler.copy_file(self.audio_narration_filename, segment_part_filename)
            print_completed('Original voice narration file copied to segment parts folder')
            self.audio_narration_filename = segment_part_filename
            self._set_audio_filename(segment_part_filename)
        else:
            segment_part_filename = self._create_segment_file('narration.wav')
            # TODO: Voice parameter need to change
            # TODO: Create voice narration
            self._set_audio_filename(self.builder.build_narration(self.text_to_narrate_sanitized_without_shortcodes, output_filename = segment_part_filename))
            print_completed('Voice narration created successfully')