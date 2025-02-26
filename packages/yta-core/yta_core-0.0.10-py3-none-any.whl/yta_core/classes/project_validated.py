"""
A project that can be stored in the database.
"""
from yta_core.classes.segment_json import SegmentJson
from dataclasses import dataclass

import json


@dataclass
class ProjectValidated:
    """
    @dataclass
    A project which information has been transformed
    from the raw json to the information we need to
    be stored in the database.

    It comes from a ProjectRaw instance that has been
    validated.
    """

    status: str
    """
    The current status of the project.
    """
    script: dict
    """
    The original script as it was read from the source
    file.
    """
    segments: list[SegmentJson]
    """
    The list of the segments once they've been read
    from the database.
    """

    @property
    def as_dict(
        self
    ):
        """
        Get the instance as a dictionary.
        """
        return {
            'status': self.status,
            'script': self.script,
            'segments': [
                segment.as_dict
                for segment in self.segments
            ]
        }
    
    @property
    def as_json(
        self
    ):
        """
        Get the instance as a json, transformed
        from the dictionary version.
        """
        return json.dumps(
            self.as_dict,
            ensure_ascii = False
        )
    
    #def init_from_database():