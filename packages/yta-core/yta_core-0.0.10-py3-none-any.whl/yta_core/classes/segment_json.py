"""
TODO: Maybe I need to move this class to another
module if I'm not sure that it fits well here
"""
from yta_core.classes.enhancement_json import EnhancementJson
from dataclasses import dataclass

import json


@dataclass
class SegmentJson:
    """
    @dataclass
    The information a Segment must hold. This
    information is about a segment that is being
    processed, so its values can be different
    from the original json because they have 
    been processed.
    """

    type: str
    url: str
    text: str
    text_to_narrate: str
    voice: str
    keywords: list[str]
    filename: str
    audio_narration_filename: str
    music: str

    enhancements: list[EnhancementJson]
    extra_params: dict
    text_to_narrate_sanitized_without_shortcodes: str
    text_to_narrate_with_simplified_shortcodes: str
    text_to_narrate_sanitized: str
    duration: float
    status: str
    created_at: str

    def __init__(self):
        """
        Initializes the instance with empty string
        values for all the attributes so we can
        fill them later and individually when
        processing.
        """
        self.type = ''
        self.url = ''
        self.text = ''
        self.text_to_narrate = ''
        self.voice = ''
        self.keywords = []
        self.filename = ''
        self.audio_narration_filename = ''
        self.music = ''
        self.enhancements = []
        self.extra_params = {}
        self.text_to_narrate_sanitized_without_shortcodes = ''
        self.text_to_narrate_with_simplified_shortcodes = ''
        self.text_to_narrate_sanitized = ''
        self.duration = 0.0
        self.status = ''
        self.created_at = ''

    @property
    def as_dict(self):
        """
        Get the instance as a dictionary.
        """
        return {
            'type': self.type,
            'url': self.url,
            'text': self.text,
            'text_to_narrate': self.text_to_narrate,
            'voice': self.voice,
            'keywords': self.keywords,
            'filename': self.filename,
            'audio_narration_filename': self.audio_narration_filename,
            'music': self.music,
            'enhancements': [
                enhancement.as_dict
                for enhancement in self.enhancements
            ],
            'extra_params': self.extra_params,
            'text_to_narrate_sanitized_without_shortcodes': self.text_to_narrate_sanitized_without_shortcodes,
            'text_to_narrate_with_simplified_shortcodes': self.text_to_narrate_with_simplified_shortcodes,
            'text_to_narrate_sanitized': self.text_to_narrate_sanitized,
            'duration': self.duration,
            'status': self.status,
            'created_at': self.created_at
        }

    @property
    def as_json(self):
        """
        Get the instance as a json, transformed
        from the dictionary version.
        """
        return json.dumps(self.as_dict)