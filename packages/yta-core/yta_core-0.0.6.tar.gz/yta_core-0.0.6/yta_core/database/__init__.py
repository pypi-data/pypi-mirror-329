"""
Module to interact with the database in which
we store the projects and their information.
"""
from yta_core.database.dataclasses import MongoResult
from yta_core.enums.field import ProjectField, ProjectBuildingField, SegmentBuildingField
from yta_core.enums.status import ProjectStatus, SegmentStatus
from yta_mongo import MongoDatabaseHandler
from yta_mongo.clients import MongoDBClient
from yta_general_utils.programming.decorators import singleton_old
from yta_general_utils.programming.validator.parameter import ParameterValidator
from bson.objectid import ObjectId
from typing import Union


# Project read from file
# Project to store in database
# Project read from database
# Project as entity


@singleton_old
class DatabaseHandler(MongoDatabaseHandler):
    """
    Class to interact with the database in which the
    projects are stored and its information and status
    is handled.

    The projects are stored in the database containing
    the mongo '_id'', a 'status', the 'script' (that
    is the whole json used to generate it and to
    compare other json files to check if existing), and
    the 'segments' field that is the one the app uses to
    handle the building data and this process.

    The 'script' must be preserved as it is, to be able
    to compare jsons and avoid duplicated projects, and
    the 'segments' field must be used by the app to keep
    the building process progress.
    """

    HOST = 'localhost:27017'
    DATABASE_NAME = 'youtube_autonomous'
    PROJECTS_TABLE_NAME = 'projects'

    def __init__(
        self
    ):
        super().__init__(
            self.HOST,
            self.DATABASE_NAME,
            MongoDBClient.LOCAL_MONGODB_COMPASS
        )

    @property
    def first_unfinished_project(
        self
    ) -> Union[MongoResult, None]:
        result = self.find_one_by_field(
            self.PROJECTS_TABLE_NAME,
            ProjectField.STATUS.value,
            { '$ne': ProjectStatus.FINISHED.value }
        )

        return (
            MongoResult(result)
            if result is not None else
            None
        )
    
    @property
    def unfinished_projects(
        self
    ) -> list[MongoResult]:
        results = self.find_by_field(
            self.PROJECTS_TABLE_NAME,
            ProjectField.STATUS.value,
            { '$ne': ProjectStatus.FINISHED.value }
        )

        return [
            MongoResult(result)
            for result in results
        ]
    
    def get_project_by_script(
        self,
        project: 'ProjectRaw'
    ) -> Union['Project', None]:
        """
        Get the project with the provided json data
        as its 'script' field.

        The script field is where the raw project
        information is stored.
        """
        from yta_core.classes.project import Project

        ParameterValidator.validate_mandatory_instance_of('project', project, 'ProjectRaw')

        project = self.find_one_by_field(
            self.PROJECTS_TABLE_NAME,
            'script',
            project.json
        )

        return (
            Project(project)
            if project is not None else
            None
        )

    def get_project_by_id(
        self,
        id: Union[ObjectId, str]
    ) -> Union['Project', None]:
        """
        Get the project with the given 'id'.
        """
        from yta_core.classes.project import Project

        ParameterValidator.validate_mandatory_instance_of('project', project, [ObjectId, str])

        project = self.find_one_by_id(
            self.PROJECTS_TABLE_NAME,
            id
        )

        return (
            Project(project)
            if project is not None else
            None
        )
    
    def insert_project(
        self,
        project: 'ProjectValidated'
    ) ->  Union['Project', None]:
        """
        Insert the provided 'project' in the database.

        This method allow inserting duplicated projects.
        """
        from yta_core.classes.project import Project

        ParameterValidator.validate_mandatory_instance_of('project', project, 'ProjectValidated')

        project = self.insert_one(
            self.PROJECTS_TABLE_NAME,
            project.as_dict
        )

        return (
            Project(project['_id'])
            if project is not None else
            None
        )
    
    def update_project_field(
        self,
        project_id: Union[ObjectId, str],
        field: str,
        value: any
    ) -> Union[MongoResult, None]:
        """
        Update the given 'field' of the project with
        the also provided 'project_id' and set the 
        'value' passed as parameter.
        """
        result = self.update_one(
            table_name = self.PROJECTS_TABLE_NAME,
            id = project_id,
            field = field,
            value = value
        )

        return (
            MongoResult(result)
            if result is not None else
            None
        )
    
    # TODO: What does it return if the update is not possible (?)
    def update_project_segment_field(
        self,
        project_id: Union[ObjectId, str],
        segment_index: int,
        field: str,
        value: any
    ) -> Union[MongoResult, None]:
        """
        Update the given 'field' of the 'segment_index'
        segment, that the project with the given 
        'project_id' has, and set the 'value' passed as
        parameter.
        """
        result = self.update_one(
            table_name = self.PROJECTS_TABLE_NAME,
            id = project_id,
            field = f'segments.{str(segment_index)}.{field}',
            value = value
        )

        return (
            MongoResult(result)
            if result is not None else
            None
        )

    # TODO: What does it return if the update is not possible (?)
    def update_project_segment_enhancement_field(
        self,
        project_id: Union[ObjectId, str],
        segment_index: int,
        enhancement_index: int,
        field: str,
        value: any
    ) -> Union[MongoResult, None]:
        """
        Update the given 'field' of the enhancement in
        the 'enhancement_index' provided position, which
        is in the 'segment_index' segment of the project
        with the given  'project_id', and set the 'value' passed as
        parameter.
        """
        result = self.update_one(
            table_name = self.PROJECTS_TABLE_NAME,
            id = project_id,
            field = f'segments.{str(segment_index)}.enhancements.{str(enhancement_index)}.{field}',
            value = value
        )

        return (
            MongoResult(result)
            if result is not None else
            None
        )
    
    def update_project_segment_status(
        self,
        project_id: Union[ObjectId, str],
        segment_index: int,
        status: str
    ) -> Union[MongoResult, None]:
        """
        Update the segment with the given 'segment_index',
        that belongs to the project with the 'project_id'
        id provided and set its status field with the given
        'status' value.
        """
        return self.update_project_segment_field(
            project_id = project_id,
            segment_index = segment_index,
            field = SegmentBuildingField.STATUS.value,
            value = status
        )
    
    def set_project_segment_as_in_progress(
        self,
        project_id: Union[ObjectId, str],
        segment_index: int
    ) -> Union[MongoResult, None]:
        """
        TODO: Write doc
        """
        return self.update_project_segment_status(
            project_id = project_id,
            segment_index = segment_index,
            status = SegmentStatus.IN_PROGRESS.value
        )
    
    def set_project_segment_as_finished(
        self,
        project_id: Union[ObjectId, str],
        segment_index: int
    ) -> Union[MongoResult, None]:
        """
        TODO: Write doc
        """
        return self.update_project_segment_status(
            project_id = project_id,
            segment_index = segment_index,
            status = SegmentStatus.FINISHED.value
        )
    
    def set_project_segment_transcription(
        self,
        project_id: Union[ObjectId, str],
        segment_index: int,
        transcription: dict
    ) -> Union[MongoResult, None]:
        """
        TODO: Write doc
        """
        return self.update_project_segment_field(
            project_id = project_id,
            segment_index = segment_index,
            field = SegmentBuildingField.TRANSCRIPTION.value,
            value = transcription
        )
    
    def set_project_segment_audio_filename(
        self,
        project_id: Union[ObjectId, str],
        segment_index: int,
        audio_filename: str
    ) -> Union[MongoResult, None]:
        """
        TODO: Write doc
        """
        return self.update_project_segment_field(
            project_id = project_id,
            segment_index = segment_index,
            field = SegmentBuildingField.AUDIO_FILENAME.value,
            value = audio_filename
        )
    
    def set_project_segment_video_filename(
        self,
        project_id: Union[ObjectId, str],
        segment_index: int,
        video_filename: str
    ) -> Union[MongoResult, None]:
        """
        TODO: Write doc
        """
        return self.update_project_segment_field(
            project_id = project_id,
            segment_index = segment_index,
            field = SegmentBuildingField.VIDEO_FILENAME.value,
            value = video_filename
        )
    
    def set_project_segment_full_filename(
        self,
        project_id: Union[ObjectId, str],
        segment_index: int,
        full_filename: str
    ) -> Union[MongoResult, None]:
        """
        TODO: Write doc
        """
        return self.update_project_segment_field(
            project_id = project_id,
            segment_index = segment_index,
            field = SegmentBuildingField.FULL_FILENAME.value,
            value = full_filename
        )
    
    def set_project_music_filename(
        self,
        project_id: Union[ObjectId, str],
        music_filename: str
    ) -> Union[MongoResult, None]:
        """
        TODO: Write doc
        """
        return self.update_project_field(
            project_id = project_id,
            field = 'music_filename',
            value = music_filename
        )
    
    def set_project_as_finished(
        self,
        project_id: Union[ObjectId, str]
    ) -> Union[MongoResult, None]:
        """
        TODO: Write doc
        """
        return self.update_project_field(
            project_id = project_id,
            field = ProjectBuildingField.STATUS.value,
            value = ProjectStatus.FINISHED.value
        )
    
    def set_project_as_in_progress(
        self,
        project_id: Union[ObjectId, str]
    ) -> Union[MongoResult, None]:
        """
        TODO: Write doc
        """
        return self.update_project_field(
            project_id = project_id,
            field = ProjectBuildingField.STATUS.value,
            value = ProjectStatus.IN_PROGRESS.value
        )