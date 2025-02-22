from yta_core.classes.segment import Segment
from yta_core.database import DatabaseHandler as ProjectDatabaseHandler
from yta_core.enums.field import ProjectBuildingField
from yta_core.enums.status import ProjectStatus, SegmentStatus
from yta_multimedia.video.utils.ffmpeg_handler import FfmpegHandler
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.validator.parameter import ParameterValidator
from bson.objectid import ObjectId
from typing import Union


class Project:
    """
    Class that represents a whole video Project, containing
    different segments that are used to build consecutively
    to end being a whole video that is this project video.
    """

    id: str = None
    """
    The stringified mongo ObjectId that identifies this
    project in the database.
    """
    _status: ProjectStatus = None
    """
    The current project status that allows us to know if
    this project has started or not, or even if it has been
    finished.
    """
    _segments: list[Segment] = None
    """
    The array that contains this project segments that are
    used to build the whole project video.
    """
    _do_update_database: bool = True
    """
    Internal variable to know if we should update the
    database value.

    _This parameter is not manually set by the user._
    """
    _database_handler: ProjectDatabaseHandler = None
    """
    Object to interact with the database and get and create
    projects.

    _This parameter is not manually set by the user._
    """

    @property
    def unfinished_segments(
        self
    ) -> list[Segment]:
        """
        Get all the segments that have not been built yet
        (they are unfinished) from this project.
        """
        return [
            segment
            for segment in self.segments
            if segment.status != SegmentStatus.FINISHED.value
        ]
    
    @property
    def status(
        self
    ):
        """
        The current project status that allows us to know
        if this project has started or not, or even if it
        has been finished.
        """
        return self._status

    @status.setter
    def status(
        self,
        status: Union[ProjectStatus, str] = ProjectStatus.TO_START
    ):
        """
        Updates the 'status' property and also updates it
        in the database if it must be done.
        """
        status = ProjectStatus.to_enum(status)

        self._status = status.value
        
        if self._do_update_database:
            self._database_handler.update_project_field(
                self.id,
                ProjectBuildingField.STATUS.value,
                status.value
            )

    @property
    def segments(
        self
    ):
        """
        The array that contains this project segments that
        are used to build the whole project video.
        """
        return self._segments

    @segments.setter
    def segments(
        self,
        segments: list[Segment]
    ):
        """
        Update the 'segments' property with the provided
        'segments' parameter. This methid will check that
        any of the provided segments are SegmentJson instances.
        """
        ParameterValidator.validate_mandatory_list_of_these_instances('segments', segments, Segment)

        self._segments = segments

    def __init__(
        self,
        id: Union[str, ObjectId]
    ):
        ParameterValidator.validate_mandatory_instance_of('id', id, [str, ObjectId])

        self.id = (
            str(id)
            if PythonValidator.is_instance(id, ObjectId) else
            id
        )
        self._database_handler = ProjectDatabaseHandler()
        self.refresh()

    def refresh(
        self
    ):
        """
        Refresh the Project data by reading it from the
        database.
        """
        project = self._database_handler.get_project_by_id(self.id)

        if project is None:
            raise Exception(f'There is no project in the database with the provided "{str(self.id)}" id.')

        self._do_update_database = False

        self.status = project.json['status']
        self.segments = [
            Segment(self.id, index, segment)
            for index, segment in enumerate(project.json['segments'])
        ]

        self._do_update_database = True
        
    def build(
        self,
        output_filename: str
    ) -> bool:
        """
        Build the Project by building each segment and
        putting them together, one after another, in 
        order. This method will only build the segments
        that have not been build yet.

        The result will be stored as 'output_filename'.
        """
        # I make, by now, 'output_filename' mandatory for this purpose
        ParameterValidator.validate_mandatory_string('output_filename', output_filename, do_accept_empty = False)

        self.status = ProjectStatus.IN_PROGRESS

        for segment in self.unfinished_segments:
            segment.build()

        self.refresh()

        unfinished_segments_len = len(self.unfinished_segments)
        if unfinished_segments_len > 0:
            raise Exception(f'There are {str(unfinished_segments_len)} segments that have not been completely built (unfinished).')
        
        # I put them together in a whole project clip
        abspath = get_project_abspath()
        full_abspath_filenames = [f'{abspath}{segment.full_filename}' for segment in self.segments]
        output_abspath = output_filename
        FfmpegHandler.concatenate_videos(full_abspath_filenames, output_abspath)

        self.status = ProjectStatus.FINISHED

        return True