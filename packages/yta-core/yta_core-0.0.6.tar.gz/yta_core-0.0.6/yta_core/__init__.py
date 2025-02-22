"""
This library is the core of Youtube Autonomous,
where all the functionalities are joint and the
magic can happen.

This library manages whole projects and is 
capable of creating awesome videos from scratch.
Using AI, video effects, audio narrations and
many more things that you'll discover inside.

- The wizard: danielalcalavalera@gmail.com
"""
from yta_core.database import DatabaseHandler
from yta_core.settings import Settings
from yta_core.classes.project_raw import ProjectRaw
from yta_core.classes.project import Project
from yta_core.database.dataclasses import MongoDBProject
from yta_general_utils.programming.decorators import singleton
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.logger import print_completed, print_in_progress
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.path import create_file_abspath
from yta_general_utils.temp import Temp


@singleton
class YTA:
    """
    The amazing Youtube Autonomous class that is
    able to magically create and edit youtube
    videos by using AI and other functionalities.
    """

    _database_handler: DatabaseHandler = None
    """
    Object to interact with the database and ge
    and create projects.
    """

    @property
    def unfinished_projects(
        self
    ) -> list[MongoDBProject]:
        """
        Get a list with the unfinished projects from
        the database. This will be empty if there are
        no unfinished projects.
        """
        return [
            MongoDBProject(project.json)
            for project in self._database_handler.unfinished_projects
        ]

    def __init__(
        self
    ):
        self._database_handler = DatabaseHandler()
        #  TODO: Complete it
        self._segments_abspath = f'{get_project_abspath()}{Settings.DEFAULT_SEGMENT_PARTS_FOLDER}/'
        self._projects_output_abspath = f'{get_project_abspath()}{Settings.DEFAULT_PROJECTS_OUTPUT_FOLDER}/'

        # We force to create the folder if it doesn't exist
        create_file_abspath(f'{self._segments_abspath}toforce')
        create_file_abspath(f'{self._projects_output_abspath}toforce')

    def purge(
        self,
        do_remove_segments_files: bool = False
    ):
        """
        Clean the temporary folder removing all the
        previously generated temporary files and also
        the segment files id the parameter
        'do_remove_segments_files' is set as True.
        """
        ParameterValidator.validate_mandatory_bool('do_remove_segments_files', do_remove_segments_files)

        Temp.clean_folder()

        if do_remove_segments_files:
            # TODO: Remove all files in self._segments_abspath folder
            pass

    def check_config(
        self
    ):
        """
        TODO: What configuration do we mean? That we
        are able to connect to db and that stuff (?)
        """
        # TODO: Check that the config is ok
        pass

    def insert_project_in_database_from_file(
        self,
        filename: str
    ) -> str:
        """
        Read the provided project content 'filename' and
        create a new project in the database if the provided
        'filename' contains a new project and is valid. If
        the information belongs to an already registered
        project, it will raise an exception.

        This method returns the new stored project mongo
        ObjectId as a string if successfully stored, or
        raises an Exception if anything went wrong.
        """
        ParameterValidator.validate_mandatory_string('filename', filename)

        project_from_file = ProjectRaw.init_from_file(filename)

        # If we are here, the raw project is valid

        # We don't want to have duplicated projects
        if self._database_handler.get_project_by_script(project_from_file):
            raise Exception('There is an existing project in the database with the same content.')

        # Ok, it doesn't exist, lets transform into a
        # ProjectForDatase and store it
        db_project = self._database_handler.insert_project(project_from_file.as_project_validated)

        print_completed('Project created in database with ObjectId = "' + str(db_project.json['_id']) + '"')

        return str(db_project.json['_id'])
    
    def _process_unfinished_projects(
        self
    ) -> bool:
        """
        Get the unfinished projects and process
        them one by one.
        """
        for db_project in self.unfinished_projects:
            print_in_progress(f'Processing project "{db_project.id}"')
            self._process_project(db_project)
            print_completed(f'Project "{db_project.id}" processed succesfully!')

        return True
    
    def _process_project(
        self,
        db_project: MongoDBProject
    ) -> bool:
        """
        Process the provided 'db_project' project, which must
        be a valid project stored in the database.
        """
        filename = f'{self._projects_output_abspath}project_{db_project.id}.mp4'

        return Project(db_project.id).build(filename)