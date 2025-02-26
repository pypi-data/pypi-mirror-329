from bson.objectid import ObjectId
from dataclasses import dataclass


@dataclass
class MongoResult:
    """
    @dataclass
    Just a mongo database result obtained from
    a query in the database. This is a wrapper
    to know what we are receiving.
    """

    json: dict
    """
    The json information as it is stored in the
    database.
    """

    @property
    def id(
        self
    ) -> ObjectId:
        """
        Get the mongo document id from its 'json' attribute
        if existing.
        """
        return self.json.get('_id', None)

# TODO: I think we are not using this one below
@dataclass
class MongoDBProject:
    """
    @dataclass
    The representation of a project in the mongo
    database, with its '_id' ObjectId and that
    stuff.

    This is what getting a project result from 
    the database must return.
    """

    id: ObjectId
    status: str
    script: str
    segments: str

    def __init__(
        self,
        json: dict
    ):
        self.id = json['_id']
        self.status = json['status']
        self.script = json['script']
        self.segments = json['segments']

        KEYS_TO_AVOID = ['_id', 'status', 'script', 'created_at']

        # Dynamically fulfill any other field
        for key, value in json.items():
            if key not in KEYS_TO_AVOID:
                setattr(self, key, value)